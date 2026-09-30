WITH dim_complaint AS (
    SELECT DISTINCT
        complaint_type,
        descriptor
    FROM {{ref('curated_311_service_requests_incremental')}}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['complaint_type', 'descriptor']) }} AS complaint_key,
    complaint_type,
    descriptor
FROM dim_complaint