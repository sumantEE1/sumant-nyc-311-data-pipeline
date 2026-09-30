{{
    config(
        materialized='incremental',
        unique_key='unique_key',
        incremental_strategy='merge'
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

)

select * from service_request_curated