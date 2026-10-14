select ocid, alertas
from {{ ref('fct_alertas_proceso') }}
where alertas not between 0 and 3
   or alertas <> participante_unico::int + plazo_corto::int + proveedor_concentrado::int
