import streamlit as st

from carga import leer

metodos = leer("metodos")

st.title("Metodología")

st.markdown("""
### Fuente

Datos abiertos de contrataciones públicas del Organismo Especializado para las Contrataciones Públicas
Eficientes (OECE), publicados en el estándar OCDS bajo licencia CC BY 4.0. Se analizan los procesos
publicados en el SEACE desde el 1 de enero de 2019. Los montos en moneda extranjera se convierten a soles
con el tipo de cambio que publica el OECE para cada adjudicación.

### Indicadores

Los indicadores siguen la guía *Red flags for integrity* de Open Contracting Partnership, adaptada a los
campos disponibles en los datos peruanos.

| Indicador | Se marca cuando |
|---|---|
| Participante único | Un proceso de un método competitivo tiene un solo participante registrado |
| Plazo corto | El plazo de consultas y observaciones es menor a la mitad de la mediana de su método |
| Proveedor concentrado | El ganador se llevó al menos el 25% del monto adjudicado por la entidad en ese año, con 3 procesos ganados o más |
| Igual al referencial | El monto adjudicado está dentro del 0.5% del valor referencial. Se muestra como contexto y no suma al conteo, porque ocurre en el 41% de los procesos |

Un método se considera competitivo cuando, a nivel nacional, menos del 10% de sus procesos tuvo un solo
participante. Así quedan fuera métodos como la Contratación Directa, donde un único participante es normal.
""")

st.markdown("**Métodos considerados competitivos**")
st.dataframe(
    metodos[metodos["es_competitivo"]].sort_values("procesos", ascending=False)[
        ["metodo_detalle", "procesos_con_participantes", "tasa_participante_unico"]
    ],
    hide_index=True,
    width="stretch",
    column_config={
        "metodo_detalle": "Método",
        "procesos_con_participantes": st.column_config.NumberColumn("Procesos", format="localized"),
        "tasa_participante_unico": st.column_config.NumberColumn("Participante único", format="percent"),
    },
)

st.markdown("""
### Qué no significa una alerta

Una alerta no prueba corrupción ni ninguna irregularidad. Un participante único puede deberse a un mercado
pequeño o muy especializado, y un proveedor concentrado puede ser el único que atiende una zona. Las alertas
sirven para priorizar qué revisar, no para sacar conclusiones.

### Limitaciones

- El dato de participantes cuenta empresas registradas en el proceso, no ofertas presentadas.
- El plazo de convocatoria no se puede usar: en los datos publicados, su inicio y su fin son siempre el mismo día.
- 54,606 procesos tienen el valor referencial reservado y no se evalúan en el indicador de igual al referencial.
- Los consorcios se identifican con un código interno del OECE, no con un RUC.

### Antecedentes

Este análisis se inspira en trabajos previos: **Funes**, de Ojo Público, que calcula el riesgo de corrupción
en las contrataciones peruanas, y **Cardinal**, la librería de indicadores de Open Contracting Partnership.

El código, el modelo de datos y las pruebas de calidad están en
[github.com/Gabriel250604/riesgo-contrataciones-peru](https://github.com/Gabriel250604/riesgo-contrataciones-peru).
""")
