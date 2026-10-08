from pyspark.sql import SparkSession

# DRIVER: this script is the driver; SparkSession is its entry point
spark = (
    SparkSession.builder
    .appName("cluster-demo")
    .master("local[2]")                       # CLUSTER MANAGER (local[2] = 2 threads on your laptop)
    # .master("yarn") or "k8s://https://host:port" on a real cluster
    .config("spark.executor.instances", "2")  # EXECUTORS: how many
    .config("spark.executor.memory", "1g")    # EXECUTORS: memory each
    .config("spark.executor.cores", "2")      # TASK slots per executor
    .getOrCreate()
)

df = spark.range(1_000_000)                   # data split into PARTITIONS
df = df.repartition(4)                        # 4 partitions = 4 TASKS per stage

result = df.filter(df.id % 2 == 0)            # transformation (lazy, DAG scheduler only records it)

result.cache()                                # CACHE: stored in executor memory
print(result.count())                         # action: DAG scheduler builds tasks, executors run them
print(df.rdd.getNumPartitions())   # partitions, which is the number of tasks in that stage
result.explain()                   # text plan showing where the Exchange (shuffle) happens
spark.stop()

