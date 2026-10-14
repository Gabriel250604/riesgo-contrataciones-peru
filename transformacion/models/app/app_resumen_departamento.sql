{{ config(location='../app/datos/resumen_departamento.parquet') }}

select
    departamento,
    count(*) as procesos,
    sum(monto_adjudicado_pen) as monto_adjudicado_pen,
    count(*) filter (where es_competitivo and participantes is not null) as procesos_competitivos,
    count(*) filter (where participante_unico) as participante_unico,
    count(*) filter (where alertas >= 1) as procesos_con_alerta
from {{ ref('fct_alertas_proceso') }}
group by departamento
order by departamento
