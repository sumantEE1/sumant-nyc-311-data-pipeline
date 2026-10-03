FROM apache/airflow:2.9.3-python3.11

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN python -m venv /home/airflow/dbt_venv \
 && /home/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-core dbt-snowflake