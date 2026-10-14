{{ config(location='../app/datos/resumen_anual.parquet') }}

select
    anio,
    count(*) as procesos,
    sum(monto_adjudicado_pen) as monto_adjudicado_pen,
    count(*) filter (where es_competitivo and participantes is not null) as procesos_competitivos,
    count(*) filter (where participante_unico) as participante_unico,
    count(*) filter (where plazo_corto) as plazo_corto,
    count(*) filter (where proveedor_concentrado) as proveedor_concentrado,
    count(*) filter (where alertas >= 1) as procesos_con_alerta
from {{ ref('fct_alertas_proceso') }}
group by anio
order by anio
