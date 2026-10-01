with fct_311_service_requests as (
    select
        unique_key,
        {{ dbt_utils.generate_surrogate_key(['complaint_type', 'descriptor']) }} as complaint_key,
        agency,
        coalesce(borough, 'Unspecified') as borough,
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
    qualify row_number() over (
        partition by unique_key
        order by ingested_at desc, created_date desc
    ) = 1
)

select * from fct_311_service_requests