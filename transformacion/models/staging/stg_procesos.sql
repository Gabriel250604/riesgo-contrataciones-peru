select
    ocid,
    id as id_version,
    buyer_id as entidad_id,
    trim(buyer_name) as entidad_nombre,
    tender_procurementMethod as metodo,
    trim(tender_procurementMethodDetails) as metodo_detalle,
    tender_mainProcurementCategory as categoria,
    trim(tender_title) as titulo,
    cast(substr(tender_datePublished, 1, 10) as date) as fecha_publicacion,
    try_cast(tender_numberOfTenderers as integer) as participantes,
    try_cast(tender_enquiryPeriod_durationInDays as integer) as dias_consultas,
    case
        when try_cast(tender_value_amount_PEN as double) > 0
            then try_cast(tender_value_amount_PEN as double)
    end as valor_referencial_pen,
    tender_hasTenderInformationProtectedByLaw = 'true' as valor_reservado,
    anio_archivo
from {{ source('bronze', 'main') }}
where tender_datePublished >= '2019'
