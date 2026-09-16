from datetime import datetime, timedelta
import os
import snowflake.connector
from snowflake.connector import connect
from airflow import DAG
from airflow.decorators import task
from airflow.exceptions import AirflowFailException
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator


import logging

logging.basicConfig(level=logging.INFO)

REQUIRED_VARIABLES = [
    "gcs_source_bucket",
    "gcs_source_object",
    "gcs_destination_bucket",
    "gcs_destination_object",
]

with DAG(
    dag_id="gcs_copy_files",
    description="Copy file(s) between two GCS locations, then load into Snowflake",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["gcs", "file-transfer", "snowflake"],
) as dag:

    copy_files = GCSToGCSOperator(
        task_id="copy_files",
        source_bucket="{{ var.value.gcs_source_bucket }}",
        source_object="{{ var.value.gcs_source_object }}",
        destination_bucket="{{ var.value.gcs_destination_bucket }}",
        destination_object="{{ var.value.gcs_destination_object }}",
        gcp_conn_id="google_cloud_default",
        move_object=False,
    )

    copy_files


SNOWFLAKE_ACCOUNT = "gusdatd-dab70621"  # "<orgname>-<account_name>" from the Snowsight URL
SNOWFLAKE_WAREHOUSE = "SNOWFLAKE_LEARNING_WH"
SNOWFLAKE_DATABASE = "DE_CROSS_SKILLING_NYC_311"
SNOWFLAKE_SCHEMA = "SUMANT_DEY_RAW"



with DAG(
    dag_id="copy_raw_data_into_snowflake",
    description="load data from GCS into Snowflake",
    start_date=datetime(2026,9, 1),
    schedule=None,
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["gcs", "file-transfer", "snowflake"],
) as dag:
    copy_raw_data = CopyFromExternalStageToSnowflakeOperator(
                task_id="copy_into_snowflake",
                schema="SUMANT_DEY_RAW",
                database="DE_CROSS_SKILLING_NYC_311",
                stage="SUMANT_GCS_BUCKET_STAGE",
                table="SUMANT_DEY_RAW_NYC_311_DATA_TABLE",
                pattern=r"311_service_requests.*",
                snowflake_conn_id="snowflake_default",
                file_format="(field_delimiter=',')",
                copy_options="ON_ERROR = 'CONTINUE'",
                columns_array=["UNIQUE_KEY","CREATED_DATE","CLOSED_DATE","AGENCY","AGENCY_NAME","COMPLAINT_TYPE","DESCRIPTOR","LOCATION_TYPE","INCIDENT_ZIP","INCIDENT_ADDRESS","STREET_NAME","CROSS_STREET_1","CROSS_STREET_2","INTERSECTION_STREET_1","INTERSECTION_STREET_2","ADDRESS_TYPE","CITY","LANDMARK","FACILITY_TYPE","STATUS","DUE_DATE","RESOLUTION_DESCRIPTION","RESOLUTION_ACTION_UPDATED_DATE","COMMUNITY_BOARD","BOROUGH","X_COORDINATE","Y_COORDINATE","PARK_FACILITY_NAME","PARK_BOROUGH","BBL","OPEN_DATA_CHANNEL_TYPE","VEHICLE_TYPE","TAXI_COMPANY_BOROUGH","TAXI_PICKUP_LOCATION","BRIDGE_HIGHWAY_NAME","BRIDGE_HIGHWAY_DIRECTION","ROAD_RAMP","BRIDGE_HIGHWAY_SEGMENT","LATITUDE","LONGITUDE","LOCATION"]
            )
    
    copy_raw_data