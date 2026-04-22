select
    document_type,
    count(*) as document_count,
    sum(amount) as total_amount,
    avg(amount) as avg_amount
from {{ ref('stg_documents') }}
group by document_type
order by total_amount desc