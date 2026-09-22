with sumant_curated as(
    select 
        extract(year from created_date) as created_year,
        extract(month from created_date) as created_month,
        {% if target.status == "Closed" %}
        TRUE
        {% else %}
        FALSE   
        {% endif %} as is_closed,
        datediff('hour' , created_date, closed_date)  as resolution_hours,
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
        "_loaded_at"
    from {{ ref('stg_311_service_requests' )}}
)

select * from sumant_curated