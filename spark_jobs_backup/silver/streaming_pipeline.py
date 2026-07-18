from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_timestamp,
    upper,
    trim
)

# =====================================================
# Create Spark Session
# =====================================================

spark = (
    SparkSession.builder
    .appName("OTT Silver Streaming Layer")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 60)
print("      OTT SILVER STREAMING PIPELINE STARTED")
print("=" * 60)

# =====================================================
# Infer Schema from Bronze Layer
# (Required for Structured Streaming)
# =====================================================

bronze_schema = (
    spark.read
    .parquet("data_lake/bronze/live_events")
    .schema
)

print("Bronze schema loaded successfully.")

# =====================================================
# Read Bronze Streaming Data
# =====================================================

bronze_df = (
    spark.readStream
    .schema(bronze_schema)
    .format("parquet")
    .load("data_lake/bronze/live_events")
)

# =====================================================
# Cleaning & Transformation
# =====================================================

silver_df = (
    bronze_df

    # Convert timestamp string -> Timestamp
    .withColumn(
        "timestamp",
        to_timestamp(col("timestamp"))
    )

    # Remove duplicate events
    .dropDuplicates(["event_id"])

    # Remove null values
    .filter(col("user_id").isNotNull())
    .filter(col("content_id").isNotNull())

    # Remove invalid watch time
    .filter(col("watch_seconds") >= 0)

    # Completion should be between 0-100
    .filter(
        (col("completion_pct") >= 0) &
        (col("completion_pct") <= 100)
    )

    # Standardize text columns
    .withColumn(
        "event_type",
        upper(trim(col("event_type")))
    )

    .withColumn(
        "device",
        trim(col("device"))
    )

    .withColumn(
        "country",
        trim(col("country"))
    )

    .withColumn(
        "content_id",
        upper(trim(col("content_id")))
    )

    .withColumn(
        "genre",
        trim(col("genre"))
    )
)

# =====================================================
# Write Silver Layer
# =====================================================

query = (
    silver_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option(
        "checkpointLocation",
        "data_lake/checkpoints/silver"
    )
    .start("data_lake/silver/live_events")
)

print("\nSilver Layer is running...")
print("Listening for Bronze events...")
print("Output directory:")
print("data_lake/silver/live_events\n")

query.awaitTermination()