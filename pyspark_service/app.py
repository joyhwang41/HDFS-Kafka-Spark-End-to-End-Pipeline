from pyspark.sql import SparkSession
from pyspark.sql.functions import split, regexp_extract, col,to_timestamp
import time

spark = SparkSession.builder.appName("logAnalyzer").getOrCreate()

attempt_limit = 40  # Maximum number of attempts to create raw_df.
attempt_count = 0  # Initial count of attempts.

while attempt_count < attempt_limit:
    try:
        raw_df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:9092") \
            .option("subscribe", "log") \
            .load() \
            .selectExpr("CAST(value AS STRING)")

        # If the DataFrame is created successfully, break out of the loop.
        break

    except Exception as e:
        # If an exception occurred, increment the attempt counter and sleep for a bit before trying again.
        attempt_count += 1
        print(f"Attempt {attempt_count} of {attempt_limit} failed with error: {e}. Retrying in 5 seconds...")
        time.sleep(5)

# If the DataFrame still isn't created after all attempts, raise an exception.
if attempt_count == attempt_limit:
    raise RuntimeError("Failed to create DataFrame after several attempts. Check Kafka service.")

df = raw_df.select(
    regexp_extract('value', r'^([^\s]+\s)', 1).alias('IP'),
    to_timestamp(regexp_extract('value', r'\[(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]', 1), "yyyy-MM-dd HH:mm:ss").alias('Timestamp'),
    regexp_extract('value', r'^.*"\w+\s+([^ ]*)\s+HTTP.*"', 1).alias('Method'),
    regexp_extract('value', r'^.*"\w+\s+([^ ]*)\s+HTTP.*"', 1).alias('Path'),
    regexp_extract('value', r'^.*"\s+([^ ]*)', 1).cast('integer').alias('Response'),
    regexp_extract('value', r'^.*"\s+([^ ]*)$', 1).cast('integer').alias('Bytes')
)

df.writeStream \
  .outputMode("append") \
  .format("parquet") \
  .option("path", "hdfs://namenode:8020/user/data/logs.parquet") \
  .option("checkpointLocation", "hdfs://namenode:8020/user/data/checkpoints") \
  .start() \
  .awaitTermination()
