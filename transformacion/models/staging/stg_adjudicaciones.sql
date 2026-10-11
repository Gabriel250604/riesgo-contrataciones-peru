with tipo_cambio as (
    select main_id, awards_id, try_cast(rate as double) as tasa
    from {{ source('bronze', 'awards_value_exchangeRates') }}
)

select
    a.main_ocid as ocid,
    a.id as adjudicacion_id,
    cast(substr(a.date, 1, 10) as date) as fecha_adjudicacion,
    try_cast(a.value_amount as double) as monto,
    a.value_currency as moneda,
    case
        when a.value_currency = 'PEN' then try_cast(a.value_amount as double)
        else try_cast(a.value_amount as double) * t.tasa
    end as monto_pen
from {{ source('bronze', 'awards') }} as a
left join tipo_cambio as t
    on t.main_id = a.main_id and t.awards_id = a.id
