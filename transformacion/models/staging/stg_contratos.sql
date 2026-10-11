select
    main_ocid as ocid,
    id as contrato_id,
    awardID as adjudicacion_id,
    cast(substr(dateSigned, 1, 10) as date) as fecha_firma,
    try_cast(value_amount as double) as monto,
    value_currency as moneda,
    try_cast(implementation_finalValue_amount as double) as monto_final,
    statusDetails as estado
from {{ source('bronze', 'contracts') }}
