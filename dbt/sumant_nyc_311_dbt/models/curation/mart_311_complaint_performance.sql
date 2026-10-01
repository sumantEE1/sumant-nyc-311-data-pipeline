{{ config(materialized='table') }}

with fct as (

    select
        complaint_key,
        coalesce(borough, 'Unspecified') as borough,
        is_closed,
        resolution_hours
    from {{ ref('fct_311_service_requests') }}
),

dim as (
    select
        complaint_key,
        complaint_type
    from {{ ref('dim_311_complaint') }}

),

joined_dim_fct as (

    select
        fct.borough,
        dim.complaint_type,
        fct.is_closed,
        fct.resolution_hours
    from fct
    inner join dim
        on fct.complaint_key = dim.complaint_key

)

select
    borough,
    complaint_type,
    count(*)                                   as total_requests,
    count_if(is_closed = true)                 as closed_requests,
    count_if(is_closed = false)                as open_requests,
    round(avg(resolution_hours), 2)            as avg_resolution_hours  -- AVG ignores NULLs
from joined_dim_fct
group by borough, complaint_type