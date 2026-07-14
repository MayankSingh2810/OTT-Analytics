"""
==========================================================
Gold Layer
Quality Statistics
Enterprise Version
==========================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc
)

from config import SILVER_DIR, GOLD_DIR


def build_quality_stats(spark):

    print("=" * 70)
    print("Building Quality Statistics")
    print("=" * 70)

    events = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    quality = (

        events

        .groupBy("quality")

        .agg(

            count("*").alias("events"),

            round(
                avg("watch_seconds") / 60,
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg("buffer_time_ms"),
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