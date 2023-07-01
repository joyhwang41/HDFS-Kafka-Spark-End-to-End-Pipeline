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


# Stream for rate limiter service
df_host = df.groupBy(
    window(df.timestamp, "20 seconds", "10 seconds"),
    df.host
).count()

query1 = df_host.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Stream for cyber security alert manager
df_response = df.filter(col("http_response") >= 400).groupBy(
    window(df.timestamp, "20 seconds", "10 seconds"),
    df.http_response
).count()

query2 = df_response.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query1.awaitTermination()
query2.awaitTermination()

