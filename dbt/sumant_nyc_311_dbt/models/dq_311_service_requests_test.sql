with bad_request as (
    select * , row_number() over (
        partition by unique_key
        order by created_date desc
    ) as rn
    from {{ ref('bad_311_requests') }} 
    ),
    nyc_311_request as (
        select * from {{ ref('stg_311_service_requests') }}
    ),
    all_requests as (
        select 
            unique_key,
            created_date,
            closed_date,
            borough,
            complaint_type,
            status
        from bad_request where rn = 1
        union all
        select 
            unique_key,
            created_date,
            closed_date,
            borough,
            complaint_type,
            status
        from nyc_311_request
    )

select * from all_requests
    
