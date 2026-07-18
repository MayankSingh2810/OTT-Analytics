from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    desc,
    col,
    lit
)


def build_country_analytics(spark):

    print("=" * 70)
    print("Building Country Analytics")
    print("=" * 70)

    # -------------------------------------------------
    # Historical Watch History
    # -------------------------------------------------

    watch = spark.read.parquet(
        "data_lake/silver/watch_history"
    )

    # -------------------------------------------------
    # Live Events
    # -------------------------------------------------

    live = spark.read.parquet(
        "data_lake/silver/live_events"
    )

    # -------------------------------------------------
    # Convert Live -> Watch Schema
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Merge Historical + Live
    # -------------------------------------------------

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # -------------------------------------------------
    # Country Analytics
    # -------------------------------------------------

    country = (
        all_watch
        .groupBy("country")
        .agg(
            count("*").alias("views"),
            avg("watch_seconds").alias("avg_watch_seconds"),
            avg("completion_pct").alias("avg_completion"),
            countDistinct("user_id").alias("unique_users")
        )
        .orderBy(desc("views"))
    )

    (
        country.write
        .mode("overwrite")
        .parquet("data_lake/gold/country_analytics")
    )

    print(f"Rows : {country.count():,}")
    print("✓ country_analytics")