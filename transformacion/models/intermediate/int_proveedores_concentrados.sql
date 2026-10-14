with base as (
    select entidad_id, year(fecha_publicacion) as anio, proveedor_id, ocid, monto_pen
    from {{ ref('fct_adjudicaciones') }}
    where monto_pen > 0
),

entidad_anio as (
    select entidad_id, anio, sum(monto_pen) as monto_total, count(distinct ocid) as procesos
    from base
    group by entidad_id, anio
),

proveedor_anio as (
    select entidad_id, anio, proveedor_id, sum(monto_pen) as monto, count(distinct ocid) as procesos
    from base
    where proveedor_id is not null
    group by entidad_id, anio, proveedor_id
)

select
    p.entidad_id,
    p.anio,
    p.proveedor_id,
    p.procesos,
    p.monto,
    e.monto_total,
    p.monto / e.monto_total as participacion
from proveedor_anio as p
inner join entidad_anio as e using (entidad_id, anio)
where e.procesos >= {{ var('min_procesos_entidad_anio') }}
  and p.procesos >= {{ var('min_procesos_proveedor') }}
  and p.monto / e.monto_total >= {{ var('min_participacion_proveedor') }}
