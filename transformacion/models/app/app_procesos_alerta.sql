{{ config(location='../app/datos/procesos_alerta.parquet') }}

with ganadores as (
    select ocid, string_agg(distinct proveedor_nombre, '; ') as ganadores
    from {{ ref('fct_adjudicaciones') }}
    group by ocid
)

select
    p.ocid,
    p.entidad_id,
    e.entidad_nombre,
    p.departamento,
    p.anio,
    p.metodo_detalle,
    p.categoria,
    p.titulo,
    p.participantes,
    p.dias_consultas,
    p.valor_referencial_pen,
    p.monto_adjudicado_pen,
    g.ganadores,
    p.participante_unico,
    p.plazo_corto,
    p.proveedor_concentrado,
    p.igual_referencial,
    p.alertas
from {{ ref('fct_alertas_proceso') }} as p
inner join {{ ref('dim_entidades') }} as e using (entidad_id)
left join ganadores as g using (ocid)
where p.alertas >= 1
