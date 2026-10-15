python3 -m venv spark-env
source ./spark-env/bin/activate


pip install jupyter
pip install pyspark==3.5.1
pip install ipykernel --it add the venv to jupyter 


```
    Install a supported Python and Java:
    bash
        brew install python@3.11 openjdk@17
    Remove the old venv and create a new one with 3.11:
    bash
        cd /Users/<user>/workspace/learning/DE_Practise/sumant-nyc-311-data-pipeline/se-spark-exercise
        deactivate 2>/dev/null
        rm -rf spark-env
        /opt/homebrew/bin/python3.11 -m venv spark-env
        source spark-env/bin/activate
        python --version        # should say 3.11.x
    Install PySpark 3.5.x or 4.x:
    bash
        pip install --upgrade pip
        pip install "pyspark==3.5.3"      # or: pip install "pyspark>=4.0"

    PySpark 4.x runs on Python 3.13 and later, but 3.11 with 3.5.3 is the safest pairing.

    Point Spark at Java 17 and at the venv's Python:
    bash
        export JAVA_HOME=$(/usr/libexec/java_home -v 17)
        export PYSPARK_PYTHON=$(which python)
        export PYSPARK_DRIVER_PYTHON=$(which python)
```

pip freeze > requirements.txt



got two objects(files)
gcloud storage cp gs://sumant_nyc311/311_service_requests_000000000000 311_service_requests_000000000000
gcloud storage cp gs://sumant_nyc311/311_service_requests_000000000001 311_service_requests_000000000001

started spark on terminal 
```pyspark```

Resilient Distributed Datasets

First group - |SQL and dataframe and data set api| Streaming |Machine learning| Graph X


### Generated post implementation
# NYC 311 Service Requests – PySpark Data Pipeline

A PySpark script that loads NYC 311 service-request data from four file formats, merges and cleans it, calculates SLA metrics, enriches free-text resolution descriptions, and writes partitioned CSV output.

## What the script does

1. **Starts Spark** in local mode (`local[4]`, 4 GB driver memory).
2. **Defines an explicit schema** (46 columns) so Spark does not have to infer types.
3. **Reads four sources**:
   - JSON (`socrata_metadata_311-service-requests-from-2010-to-present.json`)
   - CSV (`311-service-requests-from-2010-to-present.csv`)
   - Parquet (`311-service-requests-from-2010-to-present.parquet/`)
   - Text / JSON lines (`311_sample_json.txt`, read without a schema, so it has a single `value` column)
4. **Combines them** with `unionByName(..., allowMissingColumns=True)`; columns missing in one source are filled with nulls.
5. **Renames columns** to `snake_case` (e.g. `Unique Key` -> `unique_key`).
6. **Drops sparse columns**: any column with more than 80% nulls (`null_count_threshold`).
7. **Calculates SLA metrics**:
   - `is_open`: `closed_date` is null
   - `effective_closed_date`: `closed_date`, or the current timestamp if still open
   - `resolution_hours`: hours between `created_date` and `effective_closed_date`
   - `within_sla`: `True` if `resolution_hours <= SLA_HOURS` (72), `False` if above, `null` for invalid or negative values
8. **Removes duplicates** on `unique_key` and sorts by `resolution_hours` descending.
9. **Adds a `year` column** from `created_date`.
10. **Enriches `resolution_description`** with a Python UDF (`analyze_resolution`) that returns:
    - `resolution_outcome` (REPAIR, POLICE ACTION, DUPLICATE, INSUFFICIENT_CONTACT, ...)
    - `agency_action_type` (TLC_ENFORCEMENT, POLICE_INTERVENTION, STANDARD_PROCEDURE)
    - `extracted_tags` (Billing, Refusal of Service, Driver Conduct, Safety)
11. **Writes the result** as CSV, overwriting the output folder.

## Output columns

`unique_key`, `resolution_description`, `borough`, `complaint_type`, `resolution_outcome`, `agency_action_type`, `extracted_tags` (comma-separated string), `year`

## Requirements

- Python 3.9+
- Java 8, 11 or 17 (required by Spark)
- PySpark **3.4 or newer** (`TimestampNTZType` is not available in older versions)

```bash
pip install pyspark
```

## Configuration

| Setting | Location in script | Default |
|---|---|---|
| SLA threshold (hours) | `SLA_HOURS` | `72` |
| Null-percentage cutoff for dropping columns | `null_count_threshold` | `80` |
| Driver memory | `.config("spark.driver.memory", ...)` | `4g` |
| Cores | `.master("local[4]")` | 4 |
| Input paths | the four `spark.read` calls | absolute paths on the author's machine |
| Output path | `.save(...)` at the end | `.../se-spark-exercise/output` |

Update the input and output paths to match your machine before running.

## How to run

```bash
python your_script_name.py
```

or

```bash
spark-submit your_script_name.py
```

## Runtime exceptions you may hit

| Exception | Likely cause | What it means / fix |
|---|---|---|
| `pyspark.errors.AnalysisException` (path does not exist) | A file path in `spark.read` is wrong or the file is missing | Check the path and file name |
| `ZeroDivisionError` | `total_row` is 0, so `n / total_row` divides by zero | All inputs were empty; check the source files |
| `AttributeError: 'NoneType' object has no attribute 'asDict'` | `null_counts.first()` returned `None` | Happens when the DataFrame has no rows |
| `TypeError` (None values in `null_row`) | `F.sum` returns `None` on an empty DataFrame | Same root cause as above |
| `Py4JJavaError` / `SparkException` | A failure inside Spark executors (bad data, UDF failure) | Read the nested Java stack trace for the real cause |
| `java.lang.OutOfMemoryError` | The data does not fit in the 4 GB driver memory | Increase `spark.driver.memory` or process less data |
| `PythonException` inside the UDF | An error in `analyze_resolution` for some row | Test the function on sample strings |
| `UnsupportedOperationException` / `ImportError` for `TimestampNTZType` | PySpark older than 3.4 | Upgrade PySpark |
| Java not found (`JAVA_HOME is not set`) | Java is not installed | Install a supported JDK |

## Known issues and suggestions

1. **Chained `partitionBy` calls**: only the last one (`year`) takes effect. To partition by all three columns use one call: `.partitionBy("borough", "complaint_type", "year")`.
2. **Unreachable branch in the UDF**: `"Police Department reviewed your complaint"` is compared against a lowercased string, so it can never match. It also sits after the `"police"` check, which catches those rows first. Use lowercase text and put the more specific check before the general one.
3. **Text source has no schema**: `.text()` yields a single `value` column, so those rows arrive as mostly nulls after the union. Parse the JSON text (for example with `spark.read.schema(schema).json(...)` or `from_json`) if you want the data used.
4. **`F.current_timestamp()`** makes `resolution_hours` for open requests change on every run.
5. **Unused import**: `TimestampNTZType` is fine, but the `IntegerType` on `Unique Key` will null out non-numeric keys in CSV/JSON reads.
6. **Multiple `count()` and `first()` actions** trigger several full passes over the data; consider `.cache()` on `combined_df_ren`.

## Project layout (suggested)

```
se-spark-exercise/
├── data/archive/        # input files
├── output/              # generated CSV (partitioned)
├── your_script_name.py
└── README.md
```