select ocid, metodo_detalle
from {{ ref('fct_alertas_proceso') }}
where participante_unico and metodo_detalle = 'Contratación Directa'
