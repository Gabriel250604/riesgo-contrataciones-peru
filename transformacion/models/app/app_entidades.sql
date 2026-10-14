{{ config(location='../app/datos/entidades.parquet') }}

select * from {{ ref('fct_alertas_entidad') }}
