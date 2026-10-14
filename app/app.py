import streamlit as st

st.set_page_config(page_title="Riesgo en contrataciones públicas del Perú", layout="wide")

paginas = [
    st.Page("paginas/resumen.py", title="Resumen", default=True),
    st.Page("paginas/entidades.py", title="Entidades"),
    st.Page("paginas/proveedores.py", title="Proveedores"),
    st.Page("paginas/metodologia.py", title="Metodología"),
]
st.navigation(paginas).run()
