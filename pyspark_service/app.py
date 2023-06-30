from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col
from pyspark.sql.types import StringType, StructType, StructField

# Define Spark session
spark = SparkSession.builder.appName("logAnalyzer").getOrCreate()

# Define the schema of the log data
schema = StructType([
    StructField("message", StringType())
])

# Create a DataFrame representing the stream of input lines from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "log") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value").cast("string"), schema))

# Perform transformations
df = df.groupBy(
    window(df.timestamp, "1 hour"),
    df.message
).count()

# Write the DataFrame to HDFS in Parquet format
query = df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "hdfs://hdfs:9000/output.parquet") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .start()

query.awaitTermination()
