import streamlit as st

from carga import AVISO, barras, leer, participacion, porcentaje, soles

entidades = leer("entidades")
por_anio = leer("entidad_anio")
procesos = leer("procesos_alerta")
proveedor_entidad = leer("proveedor_entidad")

tasa_nacional = entidades["procesos_participante_unico"].sum() / entidades["procesos_competitivos"].sum()
directa_tipica = entidades.loc[entidades["procesos"] >= 20, "participacion_directa"].median()
nombres = entidades.set_index("entidad_id")["entidad_nombre"]

st.title("Entidades")
st.caption(AVISO)

departamento = st.selectbox("Departamento", ["Todos"] + sorted(entidades["departamento"].unique()))
candidatas = entidades if departamento == "Todos" else entidades[entidades["departamento"] == departamento]
entidad_id = st.selectbox(
    "Entidad",
    candidatas.sort_values("entidad_nombre")["entidad_id"],
    format_func=lambda i: nombres[i],
    index=None,
    placeholder="Escribe el nombre de una municipalidad, ministerio o empresa del Estado",
)

if entidad_id is None:
    st.subheader("Entidades con mayor proporción de participante único")
    st.caption("Entre las entidades con al menos 50 procesos competitivos.")
    ranking = (
        candidatas[candidatas["procesos_competitivos"] >= 50]
        .sort_values("tasa_participante_unico", ascending=False)
        .head(20)
    )
    st.dataframe(
        ranking[["entidad_nombre", "departamento", "procesos", "procesos_competitivos",
                 "procesos_participante_unico", "tasa_participante_unico"]],
        hide_index=True,
        width="stretch",
        column_config={
            "entidad_nombre": st.column_config.TextColumn("Entidad", width="medium"),
            "departamento": "Departamento",
            "procesos": st.column_config.NumberColumn("Procesos", format="localized"),
            "procesos_competitivos": st.column_config.NumberColumn("Competitivos", format="localized"),
            "procesos_participante_unico": st.column_config.NumberColumn("Con participante único", format="localized"),
            "tasa_participante_unico": st.column_config.NumberColumn("Proporción", format="percent"),
        },
    )
    st.stop()

fila = entidades.set_index("entidad_id").loc[entidad_id]
st.subheader(fila.entidad_nombre)
st.caption(f"{fila.departamento} · {int(fila.procesos):,} procesos desde 2019")

c1, c2 = st.columns(2)
c1.metric("Monto adjudicado", soles(fila.monto_adjudicado_pen))
c2.metric(
    "Participante único",
    porcentaje(fila.tasa_participante_unico),
    help=f"Promedio nacional: {porcentaje(tasa_nacional)}",
)
c3, c4 = st.columns(2)
c3.metric(
    "Monto por Contratación Directa",
    porcentaje(fila.participacion_directa),
    help=f"Valor típico entre entidades: {porcentaje(directa_tipica)}",
)
c4.metric("Proveedores concentrados", int(fila.proveedores_concentrados))

anios = por_anio[por_anio["entidad_id"] == entidad_id].sort_values("anio")
if anios["procesos_con_alerta"].sum() > 0:
    st.markdown("**Procesos con alerta por año**")
    barras(anios, "anio", "procesos_con_alerta", "Procesos con alerta", alto=240)

alertados = procesos[procesos["entidad_id"] == entidad_id].sort_values(["alertas", "anio"], ascending=False).assign(
    ganadores=lambda d: d["ganadores"].fillna("Sin ganador registrado"),
    monto_adjudicado_pen=lambda d: d["monto_adjudicado_pen"].round(0),
)
st.markdown(f"**Procesos con alerta ({len(alertados):,})**")
if alertados.empty:
    st.write("Esta entidad no tiene procesos con alertas.")
else:
    st.dataframe(
        alertados[["anio", "titulo", "metodo_detalle", "ganadores", "monto_adjudicado_pen",
                   "participante_unico", "plazo_corto", "proveedor_concentrado", "ocid"]],
        hide_index=True,
        width="stretch",
        column_config={
            "anio": st.column_config.NumberColumn("Año", format="%d"),
            "titulo": "Proceso",
            "metodo_detalle": "Método",
            "ganadores": "Ganador",
            "monto_adjudicado_pen": st.column_config.NumberColumn("Adjudicado (S/)", format="localized"),
            "participante_unico": "Participante único",
            "plazo_corto": "Plazo corto",
            "proveedor_concentrado": "Proveedor concentrado",
            "ocid": "Código OCDS",
        },
    )

concentrados = proveedor_entidad[
    (proveedor_entidad["entidad_id"] == entidad_id) & proveedor_entidad["max_participacion"].notna()
]
if not concentrados.empty:
    proveedores = leer("proveedores").set_index("proveedor_id")
    concentrados = concentrados.assign(
        proveedor=concentrados["proveedor_id"].map(proveedores["proveedor_nombre"]),
        ruc=concentrados["proveedor_id"].map(proveedores["ruc"]),
        monto_adjudicado_pen=concentrados["monto_adjudicado_pen"].round(0),
    ).sort_values("max_participacion", ascending=False)
    st.markdown("**Proveedores concentrados**")
    st.caption("Proveedores que en algún año se llevaron al menos el 25% de lo adjudicado por la entidad.")
    st.dataframe(
        concentrados[["proveedor", "ruc", "procesos_ganados", "monto_adjudicado_pen", "max_participacion"]],
        hide_index=True,
        width="stretch",
        column_config={
            "proveedor": "Proveedor",
            "ruc": "RUC",
            "procesos_ganados": st.column_config.NumberColumn("Procesos ganados", format="localized"),
            "monto_adjudicado_pen": st.column_config.NumberColumn("Adjudicado (S/)", format="localized"),
            "max_participacion": st.column_config.NumberColumn("Mayor participación anual", format="percent"),
        },
    )
