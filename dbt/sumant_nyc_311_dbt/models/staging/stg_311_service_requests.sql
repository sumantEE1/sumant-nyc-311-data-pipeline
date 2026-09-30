with sumant_staging as 
    (   select 
            unique_key,
            created_date,
            closed_date,
            agency,
            agency_name,
            complaint_type,
            descriptor,
            location_type,
            incident_zip,
            incident_address,
            street_name,
            cross_street_1,
            cross_street_2,
            intersection_street_1,
            intersection_street_2,
            address_type,
            city,
            landmark,
            facility_type,
            status,
            due_date,
            resolution_description,
            resolution_action_updated_date,
            community_board,
            borough,
            x_coordinate,
            y_coordinate,
            park_facility_name,
            park_borough,
            bbl,
            open_data_channel_type,
            vehicle_type,
            taxi_company_borough,
            taxi_pickup_location,
            bridge_highway_name,
            bridge_highway_direction,
            road_ramp,
            bridge_highway_segment,
            latitude,
            longitude,
            location,
            ingested_at

        from {{ref('raw_311_service_requests_incremental')}}
        where created_date < closed_date or closed_date is null
    )

select * from sumant_staging


-- Test the above query
--  SELECT 
--     COUNT(*) AS total_rows,
--     COUNT(created_date) AS non_null_created_date,
--     COUNT(closed_date) AS non_null_closed_date,
--     COUNT(*) - COUNT(created_date) AS null_created_date_count
-- FROM SUMANT_DEY_RAW_staging.stg_311_service_requests

-- tested it
-- SELECT community_board,created_date,closed_date,due_date,resolution_action_updated_date,park_borough FROM SUMANT_DEY_RAW_staging.stg_311_service_requests limit 5;
