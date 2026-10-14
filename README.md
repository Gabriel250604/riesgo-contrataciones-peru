# Riesgo en contrataciones públicas del Perú

Alertas de riesgo sobre 567,093 procesos de contratación publicados en el SEACE entre 2019 y 2026, con S/ 489.9 mil millones adjudicados, calculadas con los datos abiertos del OECE y los indicadores de integridad de Open Contracting Partnership.

**Tablero:** [riesgo-contrataciones-peru.streamlit.app](https://riesgo-contrataciones-peru.streamlit.app)

Los datos se actualizan solos el día 5 de cada mes.

> Una alerta no prueba una irregularidad. Señala un proceso que, según los criterios de Open Contracting Partnership, merece una revisión más cuidadosa.

## Hallazgos

- **14,732 procesos (2.6%) tienen al menos una alerta** y 101 tienen dos.
- **El participante único en métodos competitivos bajó de 3.4% en 2019 a 1.4% en 2024 y 2025.** En 2026 sube a 2.3%, aunque el año todavía está en curso.
- **El participante único es mucho más frecuente en bienes (3.1%) que en servicios (1.9%) y en obras (0.2%).**
- **Loreto es el departamento con mayor proporción de procesos con alerta (6.0%)**, seguido de San Martín (4.4%) y Ucayali (3.7%). Los más bajos son Ayacucho (1.6%) y Cusco (1.6%).
- **El salto de plazo corto en 2025 viene de los procedimientos abreviados de la Ley 32069.** De los 1,764 procesos marcados ese año, 1,425 son Licitaciones Públicas Abreviadas o Concursos Públicos Abreviados con un solo día para consultas, cuando la mediana de esos métodos es de cuatro días.
- **391 proveedores se llevaron al menos el 25% de lo adjudicado por una entidad en algún año**, en 332 entidades distintas.

## Cómo funciona

```
Datos abiertos del OECE (OCDS, un archivo por año)
  src/ingesta.py     descarga cada año y lo guarda en Parquet
  transformacion/    modelo en dbt sobre DuckDB, con pruebas de calidad
  app/               tablero en Streamlit
  GitHub Actions     repite todo el proceso cada mes
```

El modelo de dbt tiene cuatro capas:

| Capa | Contenido |
|---|---|
| staging | Limpieza y tipos de las tablas del OECE: procesos, adjudicaciones, proveedores, contratos y entidades |
| intermediate | Estadísticas por método de contratación y pares entidad y proveedor con concentración |
| marts | Hechos de procesos y adjudicaciones, dimensión de entidades y alertas por proceso, entidad y proveedor |
| app | Tablas resumidas en Parquet que lee el tablero |

Cada proceso aparece una sola vez en los archivos del OECE, en el archivo del año de su última actualización. Por eso el análisis se limita a los procesos publicados desde 2019: los anteriores solo están completos si se actualizaron después de esa fecha.

## Indicadores

| Indicador | Se marca cuando |
|---|---|
| Participante único | Un proceso de un método competitivo tiene un solo participante registrado |
| Plazo corto | El plazo de consultas y observaciones es menor a la mitad de la mediana de su método |
| Proveedor concentrado | El ganador se llevó al menos el 25% del monto adjudicado por la entidad en ese año, con 3 procesos ganados o más |
| Igual al referencial | El monto adjudicado está dentro del 0.5% del valor referencial |

Un método se considera competitivo cuando tiene al menos 500 procesos con datos de participantes y, a nivel nacional, menos del 10% de ellos tuvo un solo participante. Así quedan fuera métodos como la Contratación Directa, donde un único participante es lo normal. Con esta regla califican 15 métodos.

El indicador de igual al referencial se muestra como contexto y no suma al conteo de alertas, porque ocurre en el 41% de los procesos que tienen valor referencial y monto adjudicado.

Los umbrales están en `transformacion/dbt_project.yml` como variables, para poder cambiarlos sin tocar los modelos.

## Calidad de datos

El modelo tiene 28 pruebas que se ejecutan con cada `dbt build`: claves únicas y no nulas, relaciones entre tablas, valores permitidos y cuatro pruebas propias:

- Ningún monto es negativo.
- Las alertas por proceso están entre 0 y 3.
- Ningún proceso de Contratación Directa se marca como participante único.
- Las adjudicaciones en moneda extranjera tienen tipo de cambio. Esta prueba solo avisa: hoy hay 153 adjudicaciones sin tipo de cambio, que quedan fuera de los montos en soles.

Si una prueba falla durante la actualización mensual, el tablero no se actualiza y se queda con los últimos datos válidos.

## Limitaciones

- El dato de participantes cuenta empresas registradas en el proceso, no ofertas presentadas.
- El plazo de presentación de ofertas no se puede usar: en los datos publicados su inicio y su fin son siempre el mismo día. Por eso el indicador de plazo corto usa el periodo de consultas.
- 54,606 procesos tienen el valor referencial reservado por ley y no se evalúan en el indicador de igual al referencial.
- Los consorcios se identifican con un código interno del OECE, no con un RUC.
- Los procesos publicados antes de 2019 no se incluyen.

## Antecedentes

Este proyecto no propone una metodología nueva. Aplica de forma abierta y reproducible indicadores que ya existen:

- [Funes](https://www.open-contracting.org/2020/09/10/funes-the-corruption-detecting-algorithm-that-never-forgets/), de Ojo Público, calculó un índice de riesgo de corrupción para las contrataciones peruanas.
- [Cardinal](https://cardinal.readthedocs.io/), de Open Contracting Partnership, es una librería de indicadores de riesgo sobre datos OCDS que se ha aplicado en países como Ecuador y República Dominicana.

## Ejecutarlo localmente

Requiere Python 3.13.

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/ingesta.py
cd transformacion
dbt build
cd ..
python -m streamlit run app/app.py
```

`src/ingesta.py` acepta `--desde` y `--hasta` para cargar solo algunos años, y `--forzar` para volver a descargar los que ya están cargados.

## Estructura

```
src/ingesta.py                      descarga y conversión a Parquet
notebooks/01_perfilado.ipynb        exploración inicial de los datos de 2023
notebooks/02_bronze.ipynb           verificación de la carga
transformacion/                     proyecto dbt
app/                                tablero en Streamlit
.github/workflows/actualizacion.yml actualización mensual
```

## Fuente

Datos de contrataciones públicas del Organismo Especializado para las Contrataciones Públicas Eficientes (OECE), publicados en el estándar OCDS en el [registro de datos de Open Contracting Partnership](https://data.open-contracting.org/en/publication/135) bajo licencia CC BY 4.0.
