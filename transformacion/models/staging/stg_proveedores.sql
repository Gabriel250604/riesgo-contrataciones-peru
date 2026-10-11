select
    main_ocid as ocid,
    awards_id as adjudicacion_id,
    id as proveedor_id,
    trim(name) as proveedor_nombre,
    case
        when regexp_full_match(id, 'PE-RUC-[0-9]{11}') then substr(id, 8)
    end as ruc,
    case
        when regexp_full_match(id, 'PE-RUC-[0-9]{11}') then 'empresa'
        when regexp_full_match(id, 'PE-RUC-L[0-9]+') then 'extranjero'
        else 'consorcio'
    end as tipo_proveedor
from {{ source('bronze', 'awards_suppliers') }}
