{{
    config(
        materialized='incremental',
        unique_key='unique_key',
        incremental_strategy='delete+insert'
    )
}}
with service_request_curated as (

    select
        extract(year from created_date) as created_year,
        extract(month from created_date) as created_month,
        case when status = 'Closed' then true
             else false
        end as is_closed,
        {{ get_resolution_hours('hour', 'created_date', 'closed_date') }} as resolution_hours,
        case when {{ get_resolution_hours('hour', 'created_date', 'closed_date') }} > '{{ var("long_resolution_hours") }}'
            then true else false
        end as is_long_resolution,
        unique_key,
        agency,
        agency_name,
        borough,
        complaint_type,
        descriptor,
        status,
        created_date,
        closed_date,
        resolution_action_updated_date,
        open_data_channel_type,
        ingested_at

    from {{ ref('stg_311_service_requests') }}
    -- 1. Dynamic Window: Only process records older than 30 days from today
where ingested_at < dateadd(day, -30, current_date())

    {% if is_incremental() %}
    -- 2. Incremental logic: Grab rows newer than what is already in your warehouse
        and ingested_at > (select max(ingested_at) from {{ this }})
    {% endif %}


)

select * from service_request_curated