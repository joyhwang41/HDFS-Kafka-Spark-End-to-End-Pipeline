from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, from_json, to_timestamp, split
from pyspark.sql.types import StringType, StructType, StructField, TimestampType, IntegerType

spark = SparkSession.builder.appName("logAnalyzer").getOrCreate()

schema = StructType([
    StructField("host", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("request", StringType()),
    StructField("http_response", IntegerType()),
    StructField("bytes_sent", IntegerType())
])

raw_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "log") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

split_col = split(raw_df['value'], ' ')
df = raw_df.withColumn('host', split_col.getItem(0)) \
    .withColumn('timestamp', to_timestamp(split_col.getItem(3).substr(2, 20), "yyyy-MM-dd HH:mm:ss")) \
    .withColumn('request', split_col.getItem(5).substr(2, 1000)) \
    .withColumn('http_response', split_col.getItem(8).cast(IntegerType())) \
    .withColumn('bytes_sent', split_col.getItem(9).cast(IntegerType()))

df = df.groupBy(
    window(df.timestamp, "1 hour"),
    df.host
).count()

query = df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "hdfs://hdfs:9000/output.parquet") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .start()
# Define Spark session
