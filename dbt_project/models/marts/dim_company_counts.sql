select
    company,
    count(*) as employee_count
from {{ ref('stg_documents') }}
group by company