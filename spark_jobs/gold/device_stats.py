from pyspark.sql import functions as F
from config import SILVER_DIR, GOLD_DIR


def build_device_stats(spark):

    print("=" * 70)
    print("Building Device Statistics")
    print("=" * 70)

    # ----------------------------------------------------
    # Historical Watch History
    # ----------------------------------------------------

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    # ----------------------------------------------------
    # Live Events
    # ----------------------------------------------------

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    # Convert live events to historical schema

    live = (
        live
        .withColumn("watch_id", F.col("event_id"))
        .withColumn("watch_start", F.col("timestamp"))
        .withColumn("watch_end", F.col("timestamp"))
        .withColumn(
            "watch_minutes",
            F.round(F.col("watch_seconds") / 60, 2)
        )
        .withColumn(
            "completed",
            F.when(F.col("completion_pct") >= 90, "Yes")
             .otherwise("No")
        )
        .withColumn("liked", F.lit("No"))
        .withColumn("added_to_watchlist", F.lit("No"))
        .withColumn("recommendation_source", F.lit("Live"))
        .withColumn("engagement_level", F.lit("Live"))
        .withColumn("binge_watch", F.lit("No"))
        .select(watch.columns)
    )

    # ----------------------------------------------------
    # Historical + Live
    # ----------------------------------------------------

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    result = (

        all_watch

        .groupBy("device")

        .agg(

            F.count("*").alias("total_events"),

            F.round(
                F.avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            F.round(
                F.sum("watch_minutes") / 60,
                2
            ).alias("total_watch_hours"),

            F.round(
                F.avg("completion_pct"),
                2
            ).alias("avg_completion")

        )

        .orderBy(
            F.desc("total_events")
        )

    )

    output = GOLD_DIR / "device_stats"

    result.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {result.count():,}")
    print(f"Saved : {output}")

    return result