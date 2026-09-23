-- tests/return_invalid_requests.sql

select
    unique_key,closed_date,created_date
from {{ ref('stg_311_service_requests') }}
where closed_date < created_date