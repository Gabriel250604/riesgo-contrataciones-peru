{{ config(location='../app/datos/metodos.parquet') }}

select * from {{ ref('int_metodos') }}
