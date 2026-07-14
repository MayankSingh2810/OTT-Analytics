from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    to_date,
    countDistinct,
    count,
    avg,
    col
)

# ==========================================================
# SPARK SESSION
# ==========================================================

spark = (
    SparkSession.builder
    .appName("DailyActiveUsers")
    .getOrCreate()
)

# ==========================================================
# LOAD SILVER DATA
# ==========================================================

df = spark.read.parquet(
    "data_lake/silver/live_events"
)

# ==========================================================
# CREATE DATE COLUMN
# ==========================================================

df = df.withColumn(
    "event_date",
    to_date(col("event_time"))
)

# ==========================================================
# DAILY ACTIVE USERS
# ==========================================================

daily = (

    df.groupBy("event_date")

    .agg(

        countDistinct("user_id").alias(
            "daily_active_users"
        ),

        count("*").alias(
            "total_events"
        ),

        avg("watch_seconds").alias(
            "avg_watch_seconds"
        )

    )

    .orderBy("event_date")

)

# ==========================================================
# SAVE GOLD
# ==========================================================

output = "data_lake/gold/daily_active_users"

daily.write.mode("overwrite").parquet(output)

print("\n======================================")
print("Daily Active Users Created")
print("======================================")
print(f"Rows : {daily.count()}")
print(f"Saved : {output}")

spark.stop()