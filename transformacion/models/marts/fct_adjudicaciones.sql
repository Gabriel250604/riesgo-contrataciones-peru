select
    a.ocid || '|' || a.adjudicacion_id as adjudicacion_clave,
    a.ocid,
    a.adjudicacion_id,
    p.entidad_id,
    p.metodo,
    p.metodo_detalle,
    p.categoria,
    p.fecha_publicacion,
    a.fecha_adjudicacion,
    s.proveedor_id,
    s.ruc,
    s.proveedor_nombre,
    s.tipo_proveedor,
    a.moneda,
    a.monto,
    a.monto_pen
from {{ ref('stg_adjudicaciones') }} as a
inner join {{ ref('stg_procesos') }} as p on p.ocid = a.ocid
left join {{ ref('stg_proveedores') }} as s
    on s.ocid = a.ocid and s.adjudicacion_id = a.adjudicacion_id
