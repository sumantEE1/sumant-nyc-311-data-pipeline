Airflow GCS Pipeline - Progress Notes (2026-09-10)
Done today
 Created local Airflow setup: docker-compose.yaml (Postgres + LocalExecutor, webserver, scheduler) and Dockerfile (apache/airflow:2.9.3-python3.11, installs requirements.txt).
 Added apache-airflow-providers-google to requirements.txt.
 Created dags/gcs_copy_files.py: validate_config (PythonOperator, checks required Airflow Variables exist) -> copy_files (GCSToGCSOperator).
 Configured GCS access: mounted service account key at keys/service-account.json (read-only), set GOOGLE_APPLICATION_CREDENTIALS, and defined the google_cloud_default connection explicitly via AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT in docker-compose.yaml (plain docker compose up does NOT read airflow_settings.yaml, so that file is reference-only / for astro dev start).
 Excluded the key from git and the Docker build context (.gitignore, .dockerignore both have keys/).
 Fixed real config bugs found during review:
retry_delay was a raw int (300) instead of timedelta(minutes=5) - would have crashed on the first retry.
airflow-init's airflow users create failed on every restart after the first (user already exists) and would have blocked webserver/scheduler from starting - added || true.
Removed obsolete version: key from docker-compose.yaml.
Cleaned blank pools/variables placeholders in airflow_settings.yaml.
 Silenced unrelated exampledag.py import error (Astro's default example DAG, written for Airflow 3.x's airflow.sdk, incompatible with the 2.9.3 image here) by adding it to dags/.airflowignore.
 Diagnosed "DAG succeeded but copied 0 files":
Airflow Variables gcs_source_bucket / gcs_destination_bucket had a gs:// prefix - fixed to bare bucket names (nyc-311-dataset, sumant_nyc311).
gcs_source_object was "/", which matches nothing (GCS object names never start with /) - confirmed via a temporary debug task that listed the bucket (57 real objects, e.g. 311_service_requests_000000000000).
GCSToGCSOperator also rejects an empty string for source_object (raises "You must set source_object parameter..."), so set gcs_source_object = "*" (wildcard = whole bucket) instead of "".
Removed the temporary debug task once the fix was confirmed.
 Re-triggered the DAG - validate_config succeeded and copy_files started genuinely copying all 57 objects (~270MB each) from nyc-311-dataset to sumant_nyc311.
Still to confirm / do next
 Confirm the last triggered run (gcs_copy_files, started ~08:59 UTC) finished with state success and all 57 objects landed in sumant_nyc311 (it was still copying, file-by-file, when we last checked).
 If the old exampledag.py import error banner is still showing in the UI, run docker compose restart airflow-scheduler to force an immediate re-scan (otherwise it clears on its own within ~5 min).
 Decide on a schedule for gcs_copy_files if this should run automatically (currently schedule=None, manual trigger only).
 Note: re-running the DAG will overwrite existing objects of the same name in the destination bucket (move_object=False, no overwrite-protection configured).
 Treat keys/service-account.json as sensitive - it's a real GCP credential. It's gitignored, but don't share this folder externally without removing it first.
Key files
docker-compose.yaml / Dockerfile - local Airflow stack
dags/gcs_copy_files.py - the DAG
airflow_settings.yaml - Astro-CLI-only connection reference (not used by plain docker compose up)
keys/service-account.json - GCP service account key (gitignored)
Airflow Variables (set in UI, Admin -> Variables): gcs_source_bucket, gcs_source_object, gcs_destination_bucket, gcs_destination_object