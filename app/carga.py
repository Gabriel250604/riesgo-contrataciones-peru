from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

DATOS = Path(__file__).resolve().parent / "datos"
AZUL = "#2a78d6"
AVISO = (
    "Una alerta no prueba una irregularidad. Señala un proceso que, según los criterios de "
    "Open Contracting Partnership, merece una revisión más cuidadosa."
)


@st.cache_data
def leer(nombre):
    return pd.read_parquet(DATOS / f"{nombre}.parquet")


def soles(valor):
    if pd.isna(valor):
        return "-"
    if abs(valor) >= 1e9:
        return f"S/ {valor / 1e9:,.1f} mil millones"
    if abs(valor) >= 1e6:
        return f"S/ {valor / 1e6:,.1f} millones"
    return f"S/ {valor:,.0f}"


def porcentaje(valor):
    return "-" if pd.isna(valor) else f"{100 * valor:.1f}%"


def participacion(serie):
    return serie.map(lambda valor: "" if pd.isna(valor) else f"{100 * valor:.1f}%")


def barras(df, categoria, valor, titulo_valor, formato=",.0f", horizontal=False, alto=320):
    eje_categoria = alt.X(f"{categoria}:O", title=None, sort=None, axis=alt.Axis(labelAngle=0))
    eje_valor = alt.Y(f"{valor}:Q", title=titulo_valor, axis=alt.Axis(format=formato, gridOpacity=0.4))
    if horizontal:
        eje_categoria = alt.Y(f"{categoria}:N", title=None, sort="-x")
        eje_valor = alt.X(f"{valor}:Q", title=titulo_valor, axis=alt.Axis(format=formato, gridOpacity=0.4))
    grafico = (
        alt.Chart(df)
        .mark_bar(color=AZUL, cornerRadiusEnd=4, size=14 if horizontal else 28)
        .encode(
            x=eje_valor if horizontal else eje_categoria,
            y=eje_categoria if horizontal else eje_valor,
            tooltip=[alt.Tooltip(f"{categoria}:N", title=""), alt.Tooltip(f"{valor}:Q", title=titulo_valor, format=formato)],
        )
        .properties(height=alto)
    )
    st.altair_chart(grafico, width="stretch")
