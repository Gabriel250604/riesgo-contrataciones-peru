{{ config(location='../app/datos/proveedores.parquet') }}

select * from {{ ref('fct_alertas_proveedor') }}
