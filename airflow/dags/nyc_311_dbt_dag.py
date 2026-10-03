from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# Paths inside the Airflow container
DBT_PROJECT_DIR = "/opt/airflow/dbt_project"      # mounted from ../dbt/sumant_nyc_311_dbt
DBT_PROFILES_DIR = "/opt/airflow/dbt_profiles"    # folder containing profiles.yml
DBT_BIN = "/home/airflow/dbt_venv/bin/dbt"        # dbt installed in its own venv (see Dockerfile)

# Shared flags so every command points at the right project and profile
DBT_FLAGS = f"--project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}"

default_args = {
    "owner": "sumant",  
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="nyc_311_dbt",
    description="Run dbt models for the NYC 311 pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,        # trigger manually first; change to "@daily" later
    catchup=False,
    tags=["dbt", "nyc311"],
) as dag:

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"{DBT_BIN} deps {DBT_FLAGS}",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{DBT_BIN} run {DBT_FLAGS}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{DBT_BIN} test {DBT_FLAGS}",
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=f"{DBT_BIN} docs generate {DBT_FLAGS}",
    )

    # Serves docs at http://localhost:8081. Runs until it times out (or is marked
    # failed/success in the UI) because the web server blocks the task.
    dbt_docs_serve = BashOperator(
        task_id="dbt_docs_serve",
        bash_command=f"{DBT_BIN} docs serve {DBT_FLAGS} --host 0.0.0.0 --port 8081 --no-browser",
        execution_timeout=timedelta(hours=1),
        retries=0,
        do_xcom_push=False,
    )

    dbt_deps >> dbt_run >> dbt_test >> dbt_docs >> dbt_docs_serve