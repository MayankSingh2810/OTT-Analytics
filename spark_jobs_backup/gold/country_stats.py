from pathlib import Path

from pyspark.sql.functions import (
    avg,
    count,
    countDistinct,
    col,
    lit,
    round
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_country_stats(spark):

    print("=" * 70)
    print("Building country_stats")
    print("=" * 70)

    watch = spark.read.parquet(
        str(PROJECT_ROOT / "data_lake/silver/watch_history")
    )

    live = spark.read.parquet(
        str(PROJECT_ROOT / "data_lake/silver/live_events")
    )

    # Convert live events into watch_history format
    live = (
        live
        .withColumn("watch_minutes", round(col("watch_seconds") / 60, 2))
        .withColumn("completed",
                    (col("completion_pct") >= 90).cast("string"))
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
        .withColumn("liked", lit("No"))
        .withColumn("added_to_watchlist", lit("No"))
        .withColumn("recommendation_source", lit("Live"))
        .withColumn("engagement_level", lit("Live"))
        .withColumn("binge_watch", lit("No"))
        .select(watch.columns)
    )

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    result = (
        all_watch
        .groupBy("country")
        .agg(
            count("*").alias("views"),
            countDistinct("user_id").alias("unique_users"),
            round(avg("watch_seconds"), 2).alias("avg_watch_seconds"),
            round(avg("completion_pct"), 2).alias("avg_completion")
        )
        .orderBy(col("views").desc())
    )

    output = (
        PROJECT_ROOT
        / "data_lake"
        / "gold"
        / "country_stats"
    )

    result.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {result.count():,}")
    print("✓ country_stats completed")

    return result