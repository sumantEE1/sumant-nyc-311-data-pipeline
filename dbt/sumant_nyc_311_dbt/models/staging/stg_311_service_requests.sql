with sumant_staging as 
    (   select 
            UNIQUE_KEY as unique_key,
            TRY_TO_TIMESTAMP(CREATED_DATE, 'YYYY-MM-DD HH24:MI:SS TZD') as created_date,
            TRY_TO_TIMESTAMP(CLOSED_DATE, 'YYYY-MM-DD HH24:MI:SS TZD') as closed_date,
            AGENCY as agency,
            AGENCY_NAME as agency_name,
            COMPLAINT_TYPE as complaint_type,
            DESCRIPTOR as descriptor,
            LOCATION_TYPE as location_type,
            INCIDENT_ZIP as incident_zip,
            INCIDENT_ADDRESS as incident_address,
            STREET_NAME as street_name,
            CROSS_STREET_1 as cross_street_1,
            CROSS_STREET_2 as cross_street_2,
            INTERSECTION_STREET_1 as intersection_street_1,
            INTERSECTION_STREET_2 as intersection_street_2,
            ADDRESS_TYPE as address_type,
            CITY as city,
            LANDMARK as landmark,
            FACILITY_TYPE as facility_type,
            STATUS as status,
            TRY_TO_TIMESTAMP(DUE_DATE, 'YYYY-MM-DD HH24:MI:SS TZD') as due_date,
            RESOLUTION_DESCRIPTION as resolution_description,
            TRY_TO_TIMESTAMP(RESOLUTION_ACTION_UPDATED_DATE, 'YYYY-MM-DD HH24:MI:SS TZD') as resolution_action_updated_date,
            COMMUNITY_BOARD as community_board,
            INITCAP(TRIM(BOROUGH)) as borough,
            X_COORDINATE as x_coordinate,
            Y_COORDINATE as y_coordinate,
            PARK_FACILITY_NAME as park_facility_name,
            INITCAP(TRIM(PARK_BOROUGH)) as park_borough,
            BBL as bbl,
            OPEN_DATA_CHANNEL_TYPE as open_data_channel_type,
            VEHICLE_TYPE as vehicle_type,
            TAXI_COMPANY_BOROUGH as taxi_company_borough,
            TAXI_PICKUP_LOCATION as taxi_pickup_location,
            BRIDGE_HIGHWAY_NAME as bridge_highway_name,
            BRIDGE_HIGHWAY_DIRECTION as bridge_highway_direction,
            ROAD_RAMP as road_ramp,
            BRIDGE_HIGHWAY_SEGMENT as bridge_highway_segment,
            LATITUDE as latitude,
            LONGITUDE as longitude,
            LOCATION as location,
            TRY_TO_TIMESTAMP(CREATED_DATE, 'YYYY-MM-DD HH24:MI:SS TZD')  as ingested_at

        from {{source('raw','SUMANT_DEY_RAW_NYC_311_DATA_TABLE')}}
        where TRY_TO_TIMESTAMP(CREATED_DATE, 'YYYY-MM-DD HH24:MI:SS TZD') < TRY_TO_TIMESTAMP(CLOSED_DATE, 'YYYY-MM-DD HH24:MI:SS TZD') or CLOSED_DATE is null
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
