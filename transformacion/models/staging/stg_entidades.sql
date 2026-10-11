select
    id as entidad_id,
    trim(name) as entidad_nombre,
    upper(trim(address_department)) as departamento,
    anio_archivo,
    main_ocid as ocid
from {{ source('bronze', 'parties') }}
where roles like '%buyer%'
