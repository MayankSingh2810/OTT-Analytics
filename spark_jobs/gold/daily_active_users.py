from pyspark.sql.functions import (
    to_date,
    to_timestamp,
    countDistinct,
    count,
    avg,
    round,
    col,
    lit
)


def build_daily_active_users(spark):

    print("=" * 70)
    print("Building Daily Active Users")
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
        .select(watch.columns)
    )

    # Merge
    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    daily = (
        all_watch
        .withColumn(
            "event_date",
            to_date(
                to_timestamp(col("watch_start"))
            )
        )
        .groupBy("event_date")
        .agg(
            countDistinct("user_id").alias("daily_active_users"),
            count("*").alias("total_events"),
            round(avg("watch_minutes"), 2).alias("avg_watch_minutes")
        )
        .orderBy("event_date")
    )

    (
        daily.write
        .mode("overwrite")
        .parquet("data_lake/gold/daily_active_users")
    )

    print(f"Rows : {daily.count():,}")
    print("✓ daily_active_users")