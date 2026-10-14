{{ config(location='../app/datos/proveedor_entidad.parquet') }}

with concentrados as (
    select entidad_id, proveedor_id, max(participacion) as max_participacion
    from {{ ref('int_proveedores_concentrados') }}
    group by entidad_id, proveedor_id
)

select
    a.proveedor_id,
    a.entidad_id,
    e.entidad_nombre,
    e.departamento,
    count(distinct a.ocid) as procesos_ganados,
    sum(a.monto_pen) as monto_adjudicado_pen,
    c.max_participacion
from {{ ref('fct_adjudicaciones') }} as a
inner join {{ ref('dim_entidades') }} as e using (entidad_id)
left join concentrados as c using (entidad_id, proveedor_id)
where a.proveedor_id is not null
group by all
