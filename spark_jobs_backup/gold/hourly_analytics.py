from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    hour,
    to_timestamp,
    col,
    lit
)


def build_hourly_analytics(spark):

    print("=" * 70)
    print("Building Hourly Analytics")
    print("=" * 70)

    # Historical
    watch = spark.read.parquet(
        "data_lake/silver/watch_history"
    )

    # Live
    live = spark.read.parquet(
        "data_lake/silver/live_events"
    )

    # Convert live schema
    live = (
        live
        .withColumn("watch_minutes", round(col("watch_seconds") / 60, 2))
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
        .withColumn("liked", lit("No"))
        .withColumn("added_to_watchlist", lit("No"))
        .withColumn("recommendation_source", lit("Live"))
        .withColumn(
            "completed",
            (col("completion_pct") >= 90).cast("string")
        )
        .withColumn("engagement_level", lit("Live"))
        .withColumn("binge_watch", lit("No"))
        .withColumn(
            "hour",
            hour(to_timestamp(col("timestamp")))
        )
        .withColumn(
            "buffer_ms",
            col("buffer_time_ms")
        )
        .select(watch.columns)
    )

    # Merge
    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    hourly = (
        all_watch
        .groupBy("hour")
        .agg(
            count("*").alias("events"),
            countDistinct("user_id").alias("users"),
            round(avg("watch_seconds"), 2).alias("avg_watch"),
            round(avg("buffer_ms"), 2).alias("avg_buffer")
        )
        .orderBy("hour")
    )

    (
        hourly.write
        .mode("overwrite")
        .parquet("data_lake/gold/hourly_analytics")
    )

    print(f"Rows : {hourly.count():,}")
    print("✓ hourly_analytics")