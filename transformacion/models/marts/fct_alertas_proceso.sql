with concentrados as (
    select distinct a.ocid
    from {{ ref('fct_adjudicaciones') }} as a
    inner join {{ ref('int_proveedores_concentrados') }} as c
        on c.entidad_id = a.entidad_id
        and c.anio = year(a.fecha_publicacion)
        and c.proveedor_id = a.proveedor_id
)

select
    p.ocid,
    p.entidad_id,
    p.departamento,
    p.anio,
    p.metodo_detalle,
    p.categoria,
    p.titulo,
    p.participantes,
    p.dias_consultas,
    p.valor_referencial_pen,
    p.monto_adjudicado_pen,
    m.es_competitivo,
    coalesce(m.es_competitivo and p.participantes = 1, false) as participante_unico,
    coalesce(m.aplica_plazo and p.dias_consultas < m.mediana_dias_consultas / 2, false) as plazo_corto,
    c.ocid is not null as proveedor_concentrado,
    coalesce(p.monto_adjudicado_pen / p.valor_referencial_pen between 0.995 and 1.005, false) as igual_referencial,
    participante_unico::int + plazo_corto::int + proveedor_concentrado::int as alertas
from {{ ref('fct_procesos') }} as p
left join {{ ref('int_metodos') }} as m using (metodo_detalle)
left join concentrados as c using (ocid)
