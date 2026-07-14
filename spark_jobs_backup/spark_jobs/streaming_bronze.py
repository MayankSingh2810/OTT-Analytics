from pyspark.sql import SparkSession
from pyspark.sql.types import *

# =====================================================
# Spark Session
# =====================================================

spark = (
    SparkSession.builder
    .appName("OTT Bronze Streaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# =====================================================
# Schema
# =====================================================

schema = StructType([

    StructField("event_id", StringType(), True),
    StructField("timestamp", StringType(), True),

    StructField("user_id", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("content_id", StringType(), True),

    StructField("event_type", StringType(), True),

    StructField("device", StringType(), True),

    StructField("subscription_plan", StringType(), True),

    StructField("country", StringType(), True),

    StructField("network", StringType(), True),

    StructField("genre", StringType(), True),

    StructField("quality", StringType(), True),

    StructField("watch_seconds", IntegerType(), True),

    StructField("completion_pct", DoubleType(), True),

    StructField("buffer_time_ms", IntegerType(), True),

    StructField("rating", IntegerType(), True)

])

# =====================================================
# Read JSON Stream
# =====================================================

stream = (
    spark.readStream
    .schema(schema)
    .option("maxFilesPerTrigger", 5)
    .json("streaming/events")
)

# =====================================================
# Write Bronze Layer
# =====================================================

query = (
    stream.writeStream
    .format("parquet")
    .outputMode("append")
    .option(
        "path",
        "data_lake/bronze/live_events"
    )
    .option(
        "checkpointLocation",
        "data_lake/checkpoints/bronze"
    )
    .start()
)

print("=" * 60)
print("Bronze Streaming Started")
print("=" * 60)

query.awaitTermination()