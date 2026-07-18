"""
==========================================================
Gold Layer
Quality Statistics
LIVE + Historical
==========================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc,
    col
)

from config import SILVER_DIR, GOLD_DIR


def build_quality_stats(spark):

    print("=" * 70)
    print("Building Quality Statistics")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    live = (
        live
        .withColumn("watch_minutes", col("watch_seconds") / 60)
        .withColumn("buffer_ms", col("buffer_time_ms"))
    )

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    quality = (

        all_watch

        .groupBy("quality")

        .agg(

            count("*").alias("events"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg("buffer_ms"),
                2
            ).alias("avg_buffer_ms")

        )

        .orderBy(
            desc("events")
        )

    )

    output = GOLD_DIR / "quality_stats"

    quality.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {quality.count():,}")
    print(f"Saved : {output}")

    return quality