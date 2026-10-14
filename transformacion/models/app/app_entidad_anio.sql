{{ config(location='../app/datos/entidad_anio.parquet') }}

select
    entidad_id,
    anio,
    count(*) as procesos,
    count(*) filter (where alertas >= 1) as procesos_con_alerta
from {{ ref('fct_alertas_proceso') }}
group by entidad_id, anio
