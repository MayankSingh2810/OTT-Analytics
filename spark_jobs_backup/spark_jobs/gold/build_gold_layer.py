from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc,
    hour,
    to_timestamp,
    count_distinct
)

import os
import time
import builtins

# ==========================================================
# Spark Session
# ==========================================================

spark = (
    SparkSession.builder
    .appName("OTT Gold Analytics")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 65)
print("         BUILDING GOLD ANALYTICS LAYER")
print("=" * 65)

start = time.time()

# ==========================================================
# Paths
# ==========================================================

SILVER_PATH = "data_lake/silver/live_events"
GOLD_PATH = "data_lake/gold"

os.makedirs(GOLD_PATH, exist_ok=True)

# ==========================================================
# Load Silver Data
# ==========================================================

df = spark.read.parquet(SILVER_PATH)

print(f"\nLoaded {df.count()} Silver records.\n")

# ==========================================================
# Convert Timestamp
# ==========================================================

df = df.withColumn(
    "timestamp",
    to_timestamp("timestamp")
)

# ==========================================================
# DEVICE ANALYTICS
# ==========================================================

device_stats = (
    df.groupBy("device")
    .agg(
        count("*").alias("total_events"),
        round(avg("watch_seconds"),2).alias("avg_watch_seconds"),
        round(avg("completion_pct"),2).alias("avg_completion"),
        round(avg("rating"),2).alias("avg_rating")
    )
)

device_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/device_stats"
)

print("✓ Device Analytics Created")

# ==========================================================
# COUNTRY ANALYTICS
# ==========================================================

country_stats = (
    df.groupBy("country")
    .agg(
        count("*").alias("total_events"),
        round(avg("watch_seconds"),2).alias("avg_watch_seconds"),
        round(avg("buffer_time_ms"),2).alias("avg_buffer_ms")
    )
)

country_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/country_stats"
)

print("✓ Country Analytics Created")

# ==========================================================
# GENRE ANALYTICS
# ==========================================================

genre_stats = (
    df.groupBy("genre")
    .agg(
        count("*").alias("views"),
        round(avg("rating"),2).alias("avg_rating"),
        round(avg("completion_pct"),2).alias("completion")
    )
)

genre_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/genre_stats"
)

print("✓ Genre Analytics Created")

# ==========================================================
# SUBSCRIPTION ANALYTICS
# ==========================================================

subscription_stats = (
    df.groupBy("subscription_plan")
    .agg(
        count_distinct("user_id").alias("users"),
        count("*").alias("events"),
        round(avg("watch_seconds"),2).alias("avg_watch_seconds")
    )
)

subscription_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/subscription_stats"
)

print("✓ Subscription Analytics Created")

# ==========================================================
# EVENT ANALYTICS
# ==========================================================

event_stats = (
    df.groupBy("event_type")
    .count()
    .orderBy(desc("count"))
)

event_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/event_stats"
)

print("✓ Event Analytics Created")

# ==========================================================
# QUALITY ANALYTICS
# ==========================================================

quality_stats = (
    df.groupBy("quality")
    .agg(
        count("*").alias("events"),
        round(avg("watch_seconds"),2).alias("avg_watch")
    )
)

quality_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/quality_stats"
)

print("✓ Quality Analytics Created")

# ==========================================================
# NETWORK ANALYTICS
# ==========================================================

network_stats = (
    df.groupBy("network")
    .agg(
        count("*").alias("events"),
        round(avg("buffer_time_ms"),2).alias("avg_buffer")
    )
)

network_stats.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/network_stats"
)

print("✓ Network Analytics Created")

# ==========================================================
# TOP CONTENT
# ==========================================================

popular_content = (
    df.groupBy("content_id")
    .agg(
        count("*").alias("views")
    )
    .orderBy(desc("views"))
)

popular_content.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/popular_content"
)

print("✓ Popular Content Created")

# ==========================================================
# HOURLY TRAFFIC
# ==========================================================

hourly_usage = (
    df.withColumn(
        "hour",
        hour("timestamp")
    )
    .groupBy("hour")
    .count()
    .orderBy("hour")
)

hourly_usage.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/hourly_usage"
)

print("✓ Hourly Analytics Created")

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================
 
total_events = df.count()

unique_users = df.select("user_id").distinct().count()

unique_content = df.select("content_id").distinct().count()

avg_watch = builtins.round(
    df.select(avg("watch_seconds")).first()[0],
    2
)

avg_completion = builtins.round(
    df.select(avg("completion_pct")).first()[0],
    2
)

dashboard_summary = spark.createDataFrame(
    [
        (
            total_events,
            unique_users,
            unique_content,
            avg_watch,
            avg_completion
        )
    ],
    [
        "total_events",
        "unique_users",
        "unique_content",
        "avg_watch_seconds",
        "avg_completion"
    ]
)

dashboard_summary.write.mode("overwrite").parquet(
    f"{GOLD_PATH}/dashboard_summary"
)

print("✓ Dashboard Summary Created")


# ==========================================================
# Finish
# ==========================================================

print("\n")
print("=" * 65)
print(" GOLD LAYER CREATED SUCCESSFULLY ")
print("=" * 65)

execution_time = time.time() - start
print(f"\nExecution Time : {execution_time:.2f} seconds\n")

spark.stop()