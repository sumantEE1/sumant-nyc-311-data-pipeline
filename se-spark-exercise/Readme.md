python3 -m venv spark-env
source ./spark-env/bin/activate


pip install jupyter
pip install pyspark==3.5.1

pip freeze > requirements.txt



got two objects(files)
gcloud storage cp gs://sumant_nyc311/311_service_requests_000000000000 311_service_requests_000000000000
gcloud storage cp gs://sumant_nyc311/311_service_requests_000000000001 311_service_requests_000000000001

started spark on terminal 
```pyspark```

