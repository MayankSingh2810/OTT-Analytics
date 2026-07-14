"""
============================================================
Gold Layer
Watch Time Summary
============================================================
"""

from pyspark.sql.functions import (
    sum,
    avg,
    count,
    round
)

from config import SILVER_DIR, GOLD_DIR


def build_watch_time_summary(spark):

    print("=" * 70)
    print("Building Watch Time Summary")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    summary = (

        watch

        .agg(

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("total_watch_hours"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion_pct"),

            count("*").alias("total_watch_events")

        )

    )

    output = GOLD_DIR / "watch_time_summary"

    summary.write.mode("overwrite").parquet(str(output))

    summary.show(truncate=False)

    print(f"Saved : {output}")

    return summary