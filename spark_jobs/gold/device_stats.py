"""
============================================================
Gold Layer
Device Statistics
LIVE + Historical
============================================================
"""

from pathlib import Path

from pyspark.sql import functions as F

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER = PROJECT_ROOT / "data_lake" / "silver"
GOLD = PROJECT_ROOT / "data_lake" / "gold" / "device_stats"


def build_device_stats(spark):

    print("=" * 70)
    print("Building Device Statistics")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER / "watch_history")
    )

    live = spark.read.parquet(
        str(SILVER / "live_events")
    )

    live = (
        live
        .withColumn(
            "watch_minutes",
            F.round(F.col("watch_seconds") / 60, 2)
        )
    )

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

    result.write.mode("overwrite").parquet(
        str(GOLD)
    )

    print(f"Rows : {result.count():,}")
    print(f"Saved : {GOLD}")

    return result