with adjudicaciones as (
    select
        ocid,
        count(*) as adjudicaciones,
        count(distinct proveedor_id) as proveedores,
        sum(monto_pen) as monto_adjudicado_pen
    from {{ ref('fct_adjudicaciones') }}
    group by ocid
),

contratos as (
    select ocid, count(*) as contratos
    from {{ ref('stg_contratos') }}
    group by ocid
)

select
    p.ocid,
    p.entidad_id,
    e.departamento,
    p.metodo,
    p.metodo_detalle,
    p.categoria,
    p.titulo,
    p.fecha_publicacion,
    year(p.fecha_publicacion) as anio,
    p.participantes,
    p.dias_consultas,
    p.valor_referencial_pen,
    p.valor_reservado,
    coalesce(a.adjudicaciones, 0) as adjudicaciones,
    coalesce(a.proveedores, 0) as proveedores,
    a.monto_adjudicado_pen,
    coalesce(k.contratos, 0) as contratos
from {{ ref('stg_procesos') }} as p
left join {{ ref('dim_entidades') }} as e on e.entidad_id = p.entidad_id
left join adjudicaciones as a on a.ocid = p.ocid
left join contratos as k on k.ocid = p.ocid
