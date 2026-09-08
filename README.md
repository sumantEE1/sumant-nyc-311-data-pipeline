# sumant-nyc-311-data-pipeline
NYC data pipeline

GCP project ee-india-se-data

Target warehouse Snowflake

*** Data Profiling Findings ***

Name of database [PROFILE_NYC_311](https://app.snowflake.com/gusdatd/dab70621/#/data/databases/PROFILE_NYC_311)

Schema [CROSS_SKILLING_NYC_311](https://app.snowflake.com/gusdatd/dab70621/#/data/databases/PROFILE_NYC_311/schemas/CROSS_SKILLING_NYC_311)

Table [NYC_311_DATASET](https://app.snowflake.com/gusdatd/dab70621/#/data/databases/PROFILE_NYC_311/schemas/CROSS_SKILLING_NYC_311/table/NYC_311_DATASET)

Table definition
    ```
        create or replace TABLE PROFILE_NYC_311.CROSS_SKILLING_NYC_311.NYC_311_DATASET (
            UNIQUE_KEY NUMBER(38,0),
            CREATED_DATE VARCHAR(16777216),
            CLOSED_DATE VARCHAR(16777216),
            AGENCY VARCHAR(16777216),
            AGENCY_NAME VARCHAR(16777216),
            COMPLAINT_TYPE VARCHAR(16777216),
            DESCRIPTOR VARCHAR(16777216),
            LOCATION_TYPE VARCHAR(16777216),
            INCIDENT_ZIP VARCHAR(16777216),
            INCIDENT_ADDRESS VARCHAR(16777216),
            STREET_NAME VARCHAR(16777216),
            CROSS_STREET_1 VARCHAR(16777216),
            CROSS_STREET_2 VARCHAR(16777216),
            INTERSECTION_STREET_1 VARCHAR(16777216),
            INTERSECTION_STREET_2 VARCHAR(16777216),
            ADDRESS_TYPE VARCHAR(16777216),
            CITY VARCHAR(16777216),
            LANDMARK VARCHAR(16777216),
            FACILITY_TYPE VARCHAR(16777216),
            STATUS VARCHAR(16777216),
            DUE_DATE VARCHAR(16777216),
            RESOLUTION_DESCRIPTION VARCHAR(16777216),
            RESOLUTION_ACTION_UPDATED_DATE VARCHAR(16777216),
            COMMUNITY_BOARD VARCHAR(16777216),
            BOROUGH VARCHAR(16777216),
            X_COORDINATE NUMBER(38,0),
            Y_COORDINATE NUMBER(38,0),
            PARK_FACILITY_NAME VARCHAR(16777216),
            PARK_BOROUGH VARCHAR(16777216),
            BBL NUMBER(38,0),
            OPEN_DATA_CHANNEL_TYPE VARCHAR(16777216),
            VEHICLE_TYPE VARCHAR(16777216),
            TAXI_COMPANY_BOROUGH VARCHAR(16777216),
            TAXI_PICKUP_LOCATION VARCHAR(16777216),
            BRIDGE_HIGHWAY_NAME VARCHAR(16777216),
            BRIDGE_HIGHWAY_DIRECTION VARCHAR(16777216),
            ROAD_RAMP VARCHAR(16777216),
            BRIDGE_HIGHWAY_SEGMENT VARCHAR(16777216),
            LATITUDE FLOAT,
            LONGITUDE FLOAT,
            LOCATION VARCHAR(16777216)
        );
    ```

** Gives you table rows and type **
```DESCRIBE TABLE PROFILE_NYC_311.CROSS_SKILLING_NYC_311.NYC_311_DATASET; ```

*** Important ***
Set role , warehouse, database,schema
use role SE_DE_PARTICIPANT;
use warehouse SNOWFLAKE_LEARNING_WH
use database PROFILE_NYC_311
use schema CROSS_SKILLING_NYC_311


** Primary Key **
SHOW PRIMARY KEYS IN TABLE PROFILE_NYC_311.CROSS_SKILLING_NYC_311.NYC_311_DATASET




*** Status of ticket and count ***

    In UI set the warehouse, database and schema
    select count(*) , STATUS from NYC_311_DATASET group by STATUS;

    249339 - in progress


*** Count ***

    In UI set the warehouse, database and schema
    select count(*) from NYC_311_DATASET
    27039784

Earliest Date
    2010-01-01

```SELECT MIN(TO_DATE(CREATED_DATE,'YYYY-MM-DD HH24:MI:SS UTC')) AS earliest_order FROM NYC_311_DATASET;```

Max Date
    2021-11-08

    ```
    SELECT MAX(TO_DATE(CREATED_DATE,'YYYY-MM-DD HH24:MI:SS UTC')) AS earliest_order FROM NYC_311_DATASET;
    ```