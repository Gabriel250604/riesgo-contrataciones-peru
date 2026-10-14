select
    metodo_detalle,
    count(*) as procesos,
    count(participantes) as procesos_con_participantes,
    count(*) filter (where participantes = 1) as procesos_un_participante,
    procesos_un_participante / nullif(procesos_con_participantes, 0) as tasa_participante_unico,
    count(dias_consultas) as procesos_con_plazo,
    median(dias_consultas) as mediana_dias_consultas,
    procesos_con_participantes >= {{ var('min_procesos_metodo') }}
        and tasa_participante_unico < {{ var('max_tasa_participante_unico') }} as es_competitivo,
    procesos_con_plazo >= {{ var('min_procesos_metodo') }} as aplica_plazo
from {{ ref('fct_procesos') }}
group by metodo_detalle
