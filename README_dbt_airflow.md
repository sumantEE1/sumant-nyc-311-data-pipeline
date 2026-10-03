# Running dbt Core from Airflow (NYC 311 pipeline)

This document explains how dbt Core is run by Airflow in this repo, every step taken, the errors hit along the way, and the concepts behind them.

## 1. Architecture

```
Airflow (Docker, LocalExecutor)
 └── DAG nyc_311_dbt  (airflow/dags/nyc_311_dbt_dag.py)
      dbt_deps >> dbt_run >> dbt_test >> dbt_docs_generate >> dbt_docs_serve
           │ each task = BashOperator running the dbt CLI
           ▼
 /home/airflow/dbt_venv/bin/dbt   (dbt-core + dbt-snowflake in its own venv)
           │ reads
           ├── /opt/airflow/dbt_project   ← ../dbt/sumant_nyc_311_dbt   (mounted)
           ├── /opt/airflow/dbt_profiles  ← ../dbt/profiles             (mounted)
           └── /opt/airflow/secrets/snowflake_rsa_key.p8 ← host key     (mounted, read-only)
           ▼
        Snowflake (key-pair / SNOWFLAKE_JWT auth)
```

## 2. Step-by-step setup

| # | Step | File / command |
|---|------|----------------|
| 1 | Install dbt in an isolated venv inside the Airflow image | `airflow/Dockerfile`: `python -m venv /home/airflow/dbt_venv && pip install dbt-core dbt-snowflake` |
| 2 | Mount the dbt project, the profiles folder and the Snowflake private key into the containers | `airflow/docker-compose.yaml` (`volumes:`) |
| 3 | Tell dbt where the key is, via an env var | `SNOWFLAKE_KEY_PATH=/opt/airflow/secrets/snowflake_rsa_key.p8` in compose |
| 4 | Make the profile read the key path from that env var | `dbt/profiles/profiles.yml`: `private_key_path: "{{ env_var('SNOWFLAKE_KEY_PATH', ...) }}"` |
| 5 | Write the DAG with one `BashOperator` per dbt command | `airflow/dags/nyc_311_dbt_dag.py` |
| 6 | Rebuild and start | `cd airflow && docker compose build && docker compose up -d` |
| 7 | Run the DAG | `docker compose exec airflow-scheduler airflow dags test nyc_311_dbt` (or trigger in the UI at http://localhost:8080) |
| 8 | View the lineage graph | http://localhost:8081 (see section 7) |

Shared flags used by every task so dbt finds the right project and profile:

```
--project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_profiles
```

## 3. Errors encountered and fixes

### 3.1 Key file not found inside the container
- **Symptom:** every dbt task would fail with a file-not-found error for the private key.
- **Cause:** `dbt/profiles/profiles.yml` hardcoded `/Users/sumant/.ssh/snowflake_rsa_key.p8`. That path exists on the Mac, not in the container.
- **Fix:** read the path from `SNOWFLAKE_KEY_PATH` with `env_var(...)`, and mount the key to `/opt/airflow/secrets/snowflake_rsa_key.p8`.
- **Lesson:** paths in a profile must be valid where dbt *runs* (the container), not where you edit.

### 3.2 `psycopg2.errors.UniqueViolation: duplicate key ... "xcom_pkey"`
```
Key (dag_run_id, task_id, map_index, key)=(96, dbt_test, -1, return_value) already exists.
```
- **Symptom:** traceback in `airflow dags test`, task state `up_for_retry`.
- **Cause (two parts):**
  1. `dbt_test` failed on its first attempt, which is the real problem and is hidden above this traceback.
  2. `airflow dags test` retries inside the same DAG run. `BashOperator` pushes its last output line as an XCom `return_value`. The first attempt already stored one, so the retry's insert violates the primary key.
- **Fix / workaround:**
  - Read the real dbt error: `airflow tasks test nyc_311_dbt dbt_test <date>` (no retries, no DB state) or the attempt-1 log under `airflow/logs/`.
  - Add `do_xcom_push=False` to the operators (the output is not used) and set `retries: 0` while debugging.
- **Lesson:** the visible error is often a side effect. Look for the first failure.

### 3.3 Likely root cause of `dbt_test` failing
- `dbt run` passed, so the connection and key are fine.
- Typical reasons: a data test legitimately fails (for example the `return_invalid_request` singular test, which surfaces bad data), or a test depends on seeds that were never loaded. If seeds are the cause, add a `dbt seed` task between `dbt_deps` and `dbt_run`.

## 4. Why the Airflow `BashOperator` was required

- **dbt Core is a CLI**, not a Python library Airflow can call as a function. You run `dbt run`, `dbt test`, and so on. `BashOperator` is the simplest way for Airflow to run a command-line program and capture its exit code and logs.
- **dbt is isolated in its own venv** (`/home/airflow/dbt_venv`). Installing dbt-core and dbt-snowflake into Airflow's own Python environment risks dependency conflicts, because both pin versions of packages like `jinja2`, `pydantic` and `snowflake-connector-python`. A `PythonOperator` or `@task` would import from Airflow's interpreter and would hit those conflicts; calling the venv's binary by absolute path with `BashOperator` avoids them.
- **Exit code = task state.** dbt exits non-zero on failure and `BashOperator` marks the task failed on a non-zero exit. No glue code is needed.
- **Alternatives exist** (`DbtCloudRunJobOperator`, the Astronomer Cosmos package, `DockerOperator`, `PythonVirtualenvOperator`), but `BashOperator` is the most transparent way to learn how the pieces fit.

## 5. Tags and selectors in config

Tags are labels on dbt resources. They are set in the model's config block or in `dbt_project.yml`.

In `models/staging/raw_311_service_requests_incremental.sql`:

```sql
{{
    config(
        materialized='incremental',
        unique_key='unique_key',
        incremental_strategy='delete+insert',
        tags=['daily', 'request']
    )
}}
```

Or for a whole folder in `dbt_project.yml`:

```yaml
models:
  sumant_nyc_311_dbt:
    staging:
      +tags: ['staging']
```

Selectors choose which resources a command touches:

```bash
dbt run  --select tag:daily                 # everything tagged daily
dbt run  --select tag:request               # everything tagged request
dbt run  --select tag:daily,tag:request     # intersection (comma = AND)
dbt run  --select tag:daily tag:request     # union (space = OR)
dbt run  --select +curated_model            # a model and all its upstream parents
dbt run  --select raw_311_service_requests_incremental+   # a model and its children
dbt test --select tag:daily
```

How this ties to Airflow: tags let separate DAGs or schedules run different slices of one project, for example:

```python
BashOperator(task_id="dbt_run_daily",
             bash_command=f"{DBT_BIN} run --select tag:daily {DBT_FLAGS}")
```

Named, reusable selectors can also be defined in `selectors.yml` and called with `--selector <name>`.

## 6. Role of dbt vs role of an orchestrator

| | dbt | Airflow (orchestrator) |
|---|---|---|
| Job | **Transform** data in the warehouse with SQL | **Schedule and coordinate** tasks |
| Knows about | Models, dependencies between models (the `ref()` DAG), tests, docs | Task order, schedules, retries, alerts, cross-system dependencies |
| Runs | SQL inside Snowflake (the compute is the warehouse) | Processes that trigger things (dbt, GCS copy, etc.) |
| Dependency graph | Model-level (fine-grained) | Task-level (coarse: one task can run many models) |
| Typical question | "In what order do models build, and do they pass tests?" | "When does it run, what ran before it, and what happens if it fails?" |

dbt never moves data out of the warehouse and has no scheduler; Airflow doesn't understand SQL models. Airflow runs dbt as one step in a larger pipeline (for example GCS load, then dbt, then notifications). That is the case in this repo, where `gcs_copy_files.py` sits alongside the dbt DAG.

## 7. Failure propagation between dbt and Airflow

1. dbt finishes with an **exit code**: `0` on success, non-zero if any model errors or any test fails.
2. `BashOperator` sees that code. Non-zero marks the **Airflow task failed**.
3. Airflow applies its **retry policy**. In this DAG it is `retries=1` with a 2-minute delay, and the task shows `up_for_retry`.
4. After retries are exhausted, the task is `failed`. Its **downstream tasks become `upstream_failed`** and don't run (default trigger rule `all_success`).

Consequences in this DAG:
- If `dbt_run` fails, `dbt_test`, `dbt_docs_generate` and `dbt_docs_serve` are skipped as `upstream_failed`.
- If `dbt_test` fails, models were already built, but docs are not generated. That's why a failing test hides the lineage graph. To generate docs regardless, set `trigger_rule="all_done"` on `dbt_docs_generate`.
- Granularity is coarse: one failed model fails the whole `dbt_run` task. Airflow doesn't know which model failed; read the task log (dbt prints the failing model and SQL error). Use `--select` or the dbt artifact `target/run_results.json` for more detail. Packages like Cosmos map each model to its own Airflow task if you need per-model retries.
- Retrying `dbt_run` re-runs all selected models; incremental models are idempotent here (`delete+insert` with `unique_key`).
- `dbt test` failures can be softened per test (`severity: warn`) so they don't fail the task. Whether tests should block downstream work is a design decision.
- `airflow dags test` re-runs retries in the same DAG run, causing the XCom clash in section 3.2.

## 8. dbt docs and lineage graph

- `dbt_docs_generate` writes `manifest.json` and `catalog.json` to `dbt/sumant_nyc_311_dbt/target/` (visible on the host through the mount).
- `dbt_docs_serve` runs `dbt docs serve --host 0.0.0.0 --port 8081`. Docker publishes `8081:8081` on the `airflow-scheduler` service, because `LocalExecutor` runs tasks inside the scheduler container.
- Open **http://localhost:8081** and click the green graph icon (bottom right) for the lineage graph.
- The serve task blocks until its 1-hour `execution_timeout` (or until you mark it done). It holds a task slot, which is fine for learning but not for production.
- Without Docker you can serve from the Mac: `cd dbt/sumant_nyc_311_dbt && dbt docs serve --port 8081 --profiles-dir ../profiles`, or `cd target && python3 -m http.server 8081`.

## 9. Quick troubleshooting

| Symptom | Check |
|---|---|
| Key file not found | Is the host key path mounted, and is `SNOWFLAKE_KEY_PATH` set in the container? |
| `dbt: No such file` | Did the image rebuild (`docker compose build`) after the Dockerfile change? |
| Profile not found | Does `--profiles-dir` point to the folder containing `profiles.yml`, and does the profile name match `dbt_project.yml`? |
| `xcom_pkey` error | A task failed and was retried in `dags test`; find the first failure with `airflow tasks test` |
| Docs not reachable | Was the scheduler recreated with the new port (`docker compose up -d --force-recreate airflow-scheduler`) and is `dbt_docs_serve` running? |
| Task stays "running" forever | Expected for `dbt_docs_serve` |

## 10. Security notes
- The private key stays on the host and is mounted read-only. Don't commit it.
- `terraform.tfstate` and `.tfstate.backup` are in the repo folder; keep them out of git.
- Prefer Airflow Connections or a secrets backend over env vars and mounted keys in real deployments.
