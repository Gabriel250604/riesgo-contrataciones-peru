select ocid, 'adjudicacion' as origen, monto_pen as monto
from {{ ref('fct_adjudicaciones') }}
where monto_pen < 0
union all
select ocid, 'valor referencial', valor_referencial_pen
from {{ ref('fct_procesos') }}
where valor_referencial_pen <= 0
