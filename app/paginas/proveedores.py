import streamlit as st

from carga import AVISO, leer, participacion, porcentaje, soles

proveedores = leer("proveedores")
proveedor_entidad = leer("proveedor_entidad")

TIPOS = {"empresa": "Empresa", "consorcio": "Consorcio", "extranjero": "Extranjero"}

st.title("Proveedores")
st.caption(AVISO)

busqueda = st.text_input("Busca por RUC o nombre", placeholder="Por ejemplo: 20131257750 o constructora")

if not busqueda.strip():
    st.subheader("Proveedores que concentran el gasto de más entidades")
    st.caption("Cantidad de entidades donde el proveedor se llevó al menos el 25% de lo adjudicado en algún año.")
    ranking = proveedores[proveedores["entidades_concentradas"] > 0].sort_values(
        ["entidades_concentradas", "monto_adjudicado_pen"], ascending=False
    ).head(20).assign(monto_adjudicado_pen=lambda d: d["monto_adjudicado_pen"].round(0))
    st.dataframe(
        ranking[["proveedor_nombre", "ruc", "tipo_proveedor", "procesos_ganados", "monto_adjudicado_pen", "entidades_concentradas"]],
        hide_index=True,
        width="stretch",
        column_config={
            "proveedor_nombre": st.column_config.TextColumn("Proveedor", width="medium"),
            "ruc": "RUC",
            "tipo_proveedor": "Tipo",
            "procesos_ganados": st.column_config.NumberColumn("Procesos ganados", format="localized"),
            "monto_adjudicado_pen": st.column_config.NumberColumn("Adjudicado (S/)", format="localized"),
            "entidades_concentradas": st.column_config.NumberColumn("Entidades concentradas", format="localized"),
        },
    )
    st.stop()

texto = busqueda.strip().upper()
coincidencias = proveedores[
    proveedores["ruc"].fillna("").str.contains(texto, regex=False)
    | proveedores["proveedor_nombre"].fillna("").str.upper().str.contains(texto, regex=False)
].sort_values("monto_adjudicado_pen", ascending=False)

if coincidencias.empty:
    st.warning("No se encontró ningún proveedor con ese RUC o nombre.")
    st.stop()

nombres = coincidencias.set_index("proveedor_id")
proveedor_id = st.selectbox(
    f"{len(coincidencias):,} coincidencias, ordenadas por monto adjudicado",
    coincidencias["proveedor_id"].head(200),
    format_func=lambda i: f"{nombres.at[i, 'proveedor_nombre']} ({nombres.at[i, 'ruc'] or TIPOS[nombres.at[i, 'tipo_proveedor']]})",
)

fila = nombres.loc[proveedor_id]
st.subheader(fila.proveedor_nombre)
st.caption(f"{TIPOS[fila.tipo_proveedor]}" + (f" · RUC {fila.ruc}" if fila.ruc else ""))

c1, c2 = st.columns(2)
c1.metric("Procesos ganados", f"{int(fila.procesos_ganados):,}")
c2.metric("Monto adjudicado", soles(fila.monto_adjudicado_pen))
c3, c4 = st.columns(2)
c3.metric(
    "Ganados con participante único",
    porcentaje(fila.ganados_participante_unico / fila.procesos_ganados),
    help=f"{int(fila.ganados_participante_unico):,} procesos",
)
c4.metric("Entidades donde concentra", int(fila.entidades_concentradas))

entidades = proveedor_entidad[proveedor_entidad["proveedor_id"] == proveedor_id].sort_values(
    "monto_adjudicado_pen", ascending=False
).assign(
    monto_adjudicado_pen=lambda d: d["monto_adjudicado_pen"].round(0),
    max_participacion=lambda d: participacion(d["max_participacion"]),
)
st.markdown(f"**Entidades con las que contrató ({len(entidades):,})**")
st.dataframe(
    entidades[["entidad_nombre", "departamento", "procesos_ganados", "monto_adjudicado_pen", "max_participacion"]],
    hide_index=True,
    width="stretch",
    column_config={
        "entidad_nombre": "Entidad",
        "departamento": "Departamento",
        "procesos_ganados": st.column_config.NumberColumn("Procesos ganados", format="localized"),
        "monto_adjudicado_pen": st.column_config.NumberColumn("Adjudicado (S/)", format="localized"),
        "max_participacion": st.column_config.TextColumn("Mayor participación anual"),
    },
)
