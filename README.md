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

Create bucket with auto delete
    ```
        resource "google_storage_bucket" "auto_delete_bucket" {
            name     = "my-unique-bucket-name"
            location = "US"

            # Automatically delete files older than 30 days
            lifecycle_rule {
                condition {
                age = 30
                }
                action {
                type = "Delete"
                }
            }
        }
    ```
Upgraded Claude to enterprise
    Asked in channel #ask-claude-enterprise
    After upgrade installed Claude app 
        Switched cowork
        Gave folder access to repository aiflow folder
        
        Asked Claude
            ```Create airflow configuration
                Create an AirflowDocker compose yaml file```

            Response
                ```
                    YAML validated. I created two files in your airflow folder:

                    docker-compose.yaml — Postgres + Airflow webserver/scheduler using LocalExecutor, with an airflow-init service that migrates the DB and creates an admin user (airflow/airflow), plus mounts for dags, logs, plugins, include.
                    Dockerfile — was empty, so I filled it in to build from apache/airflow:2.9.3-python3.11 and install your requirements.txt.

                    I also added AIRFLOW_UID=50000 to your .env and created the logs/ folder (both expected by the compose file).

                    Run it with docker compose up -d, then open http://localhost:8080 (login: airflow/airflow).
                ```

Claude updated name of the file keys to service-account.json to match docker compose and airflow settings.

Added variables 
    gcs_source_bucket, gcs_source_object, gcs_destination_bucket, gcs_destination_object

Trigger the DAG either via UI or CLI
    docker compose exec airflow-webserver airflow dags trigger gcs_copy_files