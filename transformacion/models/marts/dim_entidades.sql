with ubicaciones as (
    select
        entidad_id,
        arg_max(entidad_nombre, anio_archivo) as entidad_nombre,
        arg_max(departamento, anio_archivo) as departamento
    from {{ ref('stg_entidades') }}
    group by entidad_id
)

select
    u.entidad_id,
    u.entidad_nombre,
    u.departamento,
    count(p.ocid) as procesos
from ubicaciones as u
inner join {{ ref('stg_procesos') }} as p on p.entidad_id = u.entidad_id
group by all
