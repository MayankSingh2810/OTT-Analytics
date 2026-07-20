from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("OTT Bronze Streaming")
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("event_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("user_id", StringType()),
    StructField("session_id", StringType()),
    StructField("content_id", StringType()),
    StructField("event_type", StringType()),
    StructField("device", StringType()),
    StructField("subscription_plan", StringType()),
    StructField("country", StringType()),
    StructField("network", StringType()),
    StructField("genre", StringType()),
    StructField("quality", StringType()),
    StructField("watch_seconds", IntegerType()),
    StructField("completion_pct", DoubleType()),
    StructField("buffer_time_ms", IntegerType()),
    StructField("rating", IntegerType())
])

stream = (
    spark.readStream
    .schema(schema)
    .option("maxFilesPerTrigger", 5)
    .json("streaming/events")
)

query = (
    stream.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", "data_lake/bronze/live_events")
    .option("checkpointLocation", "data_lake/checkpoints/bronze")
    .trigger(processingTime="5 seconds")
    .start()
)

print("=" * 70)
print("LIVE EVENT BRONZE STREAM STARTED")
print("=" * 70)

query.awaitTermination()