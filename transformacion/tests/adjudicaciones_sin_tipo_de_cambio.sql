{{ config(severity = 'warn') }}

select adjudicacion_clave, moneda, monto
from {{ ref('fct_adjudicaciones') }}
where moneda <> 'PEN' and monto_pen is null
