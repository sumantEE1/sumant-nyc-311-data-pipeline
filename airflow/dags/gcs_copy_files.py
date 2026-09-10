"""
DAG: gcs_copy_files
--------------------
Copies file(s) between two locations in Google Cloud Storage.

Configuration is read from Airflow Variables (Admin -> Variables in the UI),
so you can change buckets/paths without editing this file:

    gcs_source_bucket        bare bucket name, e.g. "my-source-bucket"
                              (no "gs://" prefix)
    gcs_source_object        e.g. "incoming/data.csv" for a single file, a
                              prefix like "incoming/" to copy a folder, or
                              "" (empty string) to copy everything in the
                              bucket. GCS object names never start with
                              "/", so a prefix of "/" matches nothing.
    gcs_destination_bucket   bare bucket name, e.g. "my-destination-bucket"
    gcs_destination_object   e.g. "processed/data.csv", a folder prefix, or
                              "" to keep the same names at the bucket root

Requires:
    - apache-airflow-providers-google  (add to requirements.txt)
    - An Airflow connection named "google_cloud_default" with access to
      both the source and destination buckets (Admin -> Connections).
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

REQUIRED_VARIABLES = [
    "gcs_source_bucket",
    "gcs_source_object",
    "gcs_destination_bucket",
    "gcs_destination_object",
]


def validate_config(**context):
    """
    Reads the required Airflow Variables and fails the task early, with a
    clear message, if any are missing.

    Variable.get() raises a KeyError when a variable doesn't exist. We
    catch that specific exception (rather than a bare 'except') so we
    only handle the error we expect, and re-raise it as an
    AirflowFailException -- this marks the task as Failed (not just an
    error in the logs) and stops the DAG from moving on to the copy step
    with bad/missing config.
    """
    config = {}
    missing = []

    for var_name in REQUIRED_VARIABLES:
        try:
            config[var_name] = Variable.get(var_name)
        except KeyError:
            missing.append(var_name)

    if missing:
        raise AirflowFailException(
            "Missing required Airflow Variable(s): "
            f"{', '.join(missing)}. Set them under Admin -> Variables "
            "before running this DAG."
        )

    # Push the validated config to XCom so downstream tasks/logs can use it.
    context["ti"].xcom_push(key="gcs_config", value=config)
    return config


with DAG(
    dag_id="gcs_copy_files",
    description="Copy file(s) between two GCS locations",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # trigger manually; change to a cron string to automate
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["gcs", "file-transfer"],
) as dag:

    validate = PythonOperator(
        task_id="validate_config",
        python_callable=validate_config,
    )

    copy_files = GCSToGCSOperator(
        task_id="copy_files",
        source_bucket="{{ var.value.gcs_source_bucket }}",
        source_object="{{ var.value.gcs_source_object }}",
        destination_bucket="{{ var.value.gcs_destination_bucket }}",
        destination_object="{{ var.value.gcs_destination_object }}",
        gcp_conn_id="google_cloud_default",
        # Set to True to also remove the source file(s) after copying (move
        # instead of copy). Leave False to keep the originals in place.
        move_object=False,
    )

    validate >> copy_files
