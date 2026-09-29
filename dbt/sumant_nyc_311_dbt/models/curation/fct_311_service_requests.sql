with fct_311_service_requests as (
    select 
        unique_key,
        {{ dbt_utils.generate_surrogate_key([
                "coalesce(trim(lower(complaint_type)), '')", 
                "coalesce(trim(lower(descriptor)), '')"
            ]) 
        }} as complaint_key,
        agency,
        borough,
        status,
        open_data_channel_type,
        created_date,
        closed_date,
        resolution_action_updated_date,
        created_year,
        created_month,
        is_closed,
        resolution_hours,
        ingested_at
    from {{ ref('curated_311_service_requests_incremental') }}
)

select * from fct_311_service_requests