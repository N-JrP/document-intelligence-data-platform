select
    document_type,
    count(*) as document_count
from {{ ref('stg_documents') }}
group by document_type
order by document_count desc