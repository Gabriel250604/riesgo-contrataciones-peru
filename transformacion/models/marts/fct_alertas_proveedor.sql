with adjudicaciones as (
    select
        a.proveedor_id,
        arg_max(a.proveedor_nombre, a.fecha_publicacion) as proveedor_nombre,
        any_value(a.ruc) as ruc,
        any_value(a.tipo_proveedor) as tipo_proveedor,
        count(distinct a.ocid) as procesos_ganados,
        sum(a.monto_pen) as monto_adjudicado_pen,
        count(distinct a.entidad_id) as entidades,
        count(distinct a.ocid) filter (where p.participante_unico) as ganados_participante_unico,
        count(distinct a.ocid) filter (where p.alertas >= 2) as ganados_dos_o_mas_alertas
    from {{ ref('fct_adjudicaciones') }} as a
    inner join {{ ref('fct_alertas_proceso') }} as p using (ocid)
    where a.proveedor_id is not null
    group by a.proveedor_id
),

concentracion as (
    select proveedor_id, count(distinct entidad_id) as entidades_concentradas
    from {{ ref('int_proveedores_concentrados') }}
    group by proveedor_id
)

select
    a.*,
    coalesce(c.entidades_concentradas, 0) as entidades_concentradas
from adjudicaciones as a
left join concentracion as c using (proveedor_id)
