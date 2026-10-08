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

