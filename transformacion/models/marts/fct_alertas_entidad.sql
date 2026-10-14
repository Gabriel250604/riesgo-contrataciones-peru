with procesos as (
    select
        entidad_id,
        count(*) as procesos,
        sum(monto_adjudicado_pen) as monto_adjudicado_pen,
        count(*) filter (where es_competitivo and participantes is not null) as procesos_competitivos,
        count(*) filter (where participante_unico) as procesos_participante_unico,
        count(*) filter (where plazo_corto) as procesos_plazo_corto,
        count(*) filter (where proveedor_concentrado) as procesos_proveedor_concentrado,
        count(*) filter (where alertas >= 2) as procesos_dos_o_mas_alertas
    from {{ ref('fct_alertas_proceso') }}
    group by entidad_id
),

directas as (
    select
        entidad_id,
        sum(monto_pen) filter (where metodo_detalle = 'Contratación Directa') / nullif(sum(monto_pen), 0)
            as participacion_directa
    from {{ ref('fct_adjudicaciones') }}
    group by entidad_id
),

concentracion as (
    select entidad_id, count(distinct proveedor_id) as proveedores_concentrados, max(participacion) as max_participacion
    from {{ ref('int_proveedores_concentrados') }}
    group by entidad_id
)

select
    e.entidad_id,
    e.entidad_nombre,
    e.departamento,
    p.procesos,
    p.monto_adjudicado_pen,
    p.procesos_competitivos,
    p.procesos_participante_unico,
    p.procesos_participante_unico / nullif(p.procesos_competitivos, 0) as tasa_participante_unico,
    p.procesos_plazo_corto,
    p.procesos_proveedor_concentrado,
    p.procesos_dos_o_mas_alertas,
    d.participacion_directa,
    coalesce(c.proveedores_concentrados, 0) as proveedores_concentrados,
    c.max_participacion
from {{ ref('dim_entidades') }} as e
inner join procesos as p using (entidad_id)
left join directas as d using (entidad_id)
left join concentracion as c using (entidad_id)
