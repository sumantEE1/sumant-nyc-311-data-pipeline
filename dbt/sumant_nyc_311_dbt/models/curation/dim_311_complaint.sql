with dim_complaint as (
    select 
        {{ 
            dbt_utils.generate_surrogate_key([
                "LOWER(TRIM(complaint_type))", 
                "LOWER(TRIM(descriptor))"
            ]) 
        }} AS complaint_key,
        complaint_type,
        descriptor
    from {{ref('curated_311_service_requests_incremental')}}
)

select * from dim_complaint