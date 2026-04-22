select
    status,
    count(*) as document_count
from {{ ref('stg_documents') }}
group by status
order by document_count desc