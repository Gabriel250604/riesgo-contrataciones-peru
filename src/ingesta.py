import argparse
import shutil
import tarfile
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import duckdb

URL = "https://data.open-contracting.org/en/publication/135/download?name={anio}.csv.tar.gz"
TABLAS = ["main", "awards", "awards_suppliers", "awards_value_exchangeRates", "contracts", "parties"]
FILTROS = {"parties": "WHERE roles LIKE '%buyer%'"}

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
BRONZE = RAIZ / "data" / "bronze"


def descargar(anio):
    destino = RAW / f"{anio}.csv.tar.gz"
    if destino.exists():
        return destino
    RAW.mkdir(parents=True, exist_ok=True)
    parcial = RAW / f"{anio}.descargando"
    pedido = urllib.request.Request(URL.format(anio=anio), headers={"User-Agent": "riesgo-contrataciones-peru"})
    with urllib.request.urlopen(pedido, timeout=300) as respuesta, open(parcial, "wb") as archivo:
        shutil.copyfileobj(respuesta, archivo, length=1024 * 1024)
    parcial.rename(destino)
    return destino


def extraer(archivo, anio):
    carpeta = RAW / f"{anio}_tablas"
    carpeta.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archivo, "r:gz") as tar:
        for miembro in tar:
            nombre = Path(miembro.name).name
            if miembro.isfile() and nombre.removesuffix(".csv") in TABLAS:
                miembro.name = nombre
                tar.extract(miembro, carpeta, filter="data")
    return carpeta


def convertir(carpeta, anio, con):
    filas = {}
    for tabla in TABLAS:
        csv = carpeta / f"{tabla}.csv"
        if not csv.exists():
            filas[tabla] = 0
            continue
        salida = BRONZE / tabla / f"{anio}.parquet"
        salida.parent.mkdir(parents=True, exist_ok=True)
        con.execute(f"""
            COPY (
                SELECT *, {anio} AS anio_archivo
                FROM read_csv('{csv.as_posix()}', all_varchar = true)
                {FILTROS.get(tabla, "")}
            ) TO '{salida.as_posix()}' (FORMAT parquet, COMPRESSION zstd)
        """)
        filas[tabla] = con.execute(f"SELECT count(*) FROM '{salida.as_posix()}'").fetchone()[0]
    return filas


def cargado(anio):
    return all((BRONZE / tabla / f"{anio}.parquet").exists() for tabla in ("main", "awards", "contracts"))


def procesar(anio, con, conservar=False):
    inicio = time.time()
    archivo = descargar(anio)
    megas = archivo.stat().st_size / 1e6
    carpeta = extraer(archivo, anio)
    filas = convertir(carpeta, anio, con)
    shutil.rmtree(carpeta)
    if not conservar:
        archivo.unlink()
    print(f"{anio}: {megas:,.0f} MB, {filas['main']:,} procesos, {filas['awards']:,} adjudicaciones, "
          f"{filas['contracts']:,} contratos ({time.time() - inicio:,.0f} s)")


def main():
    parser = argparse.ArgumentParser(description="Descarga los datos OCDS del OECE y los guarda en Parquet.")
    parser.add_argument("--desde", type=int, default=2019)
    parser.add_argument("--hasta", type=int, default=date.today().year)
    parser.add_argument("--forzar", action="store_true", help="vuelve a cargar los años ya procesados")
    parser.add_argument("--conservar", action="store_true", help="no borra el archivo comprimido")
    args = parser.parse_args()

    con = duckdb.connect()
    for anio in range(args.desde, args.hasta + 1):
        if cargado(anio) and not args.forzar:
            print(f"{anio}: ya estaba cargado")
            continue
        try:
            procesar(anio, con, args.conservar)
        except urllib.error.URLError as error:
            print(f"{anio}: no se pudo descargar ({error})")


if __name__ == "__main__":
    main()
