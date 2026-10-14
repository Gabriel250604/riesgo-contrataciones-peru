import altair as alt
import streamlit as st

from carga import AVISO, AZUL, leer, porcentaje, soles

anual = leer("resumen_anual")
departamentos = leer("resumen_departamento")
total = anual.sum(numeric_only=True)
ultimo = int(anual["anio"].max())

st.title("Riesgo en las contrataciones públicas del Perú")
st.caption(f"Procesos publicados en el SEACE entre 2019 y {ultimo}, a partir de los datos abiertos del OECE.")

c1, c2 = st.columns(2)
c1.metric("Procesos analizados", f"{int(total.procesos):,}")
c2.metric("Monto adjudicado", soles(total.monto_adjudicado_pen))
c3, c4 = st.columns(2)
c3.metric("Procesos con al menos una alerta", f"{int(total.procesos_con_alerta):,}")
c4.metric(
    "Participante único en métodos competitivos",
    porcentaje(total.participante_unico / total.procesos_competitivos),
)
st.info(AVISO)

st.subheader("Participante único en procesos competitivos, por año")
st.caption(f"Porcentaje de procesos competitivos con un solo participante registrado. {ultimo} está en curso.")
anual["tasa"] = anual["participante_unico"] / anual["procesos_competitivos"]
linea = (
    alt.Chart(anual)
    .mark_line(color=AZUL, strokeWidth=2, point=alt.OverlayMarkDef(color=AZUL, size=70, filled=True))
    .encode(
        x=alt.X("anio:O", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("tasa:Q", title=None, axis=alt.Axis(format=".1%", gridOpacity=0.4), scale=alt.Scale(zero=True)),
        tooltip=[
            alt.Tooltip("anio:O", title="Año"),
            alt.Tooltip("tasa:Q", title="Participante único", format=".2%"),
            alt.Tooltip("participante_unico:Q", title="Procesos", format=","),
            alt.Tooltip("procesos_competitivos:Q", title="Procesos competitivos", format=","),
        ],
    )
    .properties(height=300)
)
st.altair_chart(linea, width="stretch")

st.subheader("Procesos con alerta por departamento")
st.caption("Porcentaje de los procesos de cada departamento que tiene al menos una alerta.")
departamentos["tasa"] = departamentos["procesos_con_alerta"] / departamentos["procesos"]
barras = (
    alt.Chart(departamentos)
    .mark_bar(color=AZUL, cornerRadiusEnd=4, size=14)
    .encode(
        y=alt.Y("departamento:N", title=None, sort="-x"),
        x=alt.X("tasa:Q", title=None, axis=alt.Axis(format=".1%", gridOpacity=0.4)),
        tooltip=[
            alt.Tooltip("departamento:N", title="Departamento"),
            alt.Tooltip("tasa:Q", title="Con alerta", format=".2%"),
            alt.Tooltip("procesos_con_alerta:Q", title="Procesos con alerta", format=","),
            alt.Tooltip("procesos:Q", title="Procesos", format=","),
        ],
    )
    .properties(height=620)
)
st.altair_chart(barras, width="stretch")
