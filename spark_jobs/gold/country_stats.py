"""
============================================================
Gold Layer
Country Statistics
Enterprise Version
============================================================
"""

from pathlib import Path

from pyspark.sql.functions import (
    avg,
    count,
    col,
    round
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_country_stats(spark):

    print("=" * 70)
    print("Building Country Statistics")
    print("=" * 70)

    silver = (
        PROJECT_ROOT
        / "data_lake"
        / "silver"
        / "live_events"
    )

    df = spark.read.parquet(str(silver))

    result = (

        df

        .groupBy("country")

        .agg(

            count("*").alias("total_events"),

            round(
                avg("watch_seconds"),
                2
            ).alias("avg_watch_seconds"),

            round(
                avg("buffer_time_ms"),
                2
            ).alias("avg_buffer_ms"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion")

        )

        .orderBy(
            col("total_events").desc()
        )

    )

    output = (
        PROJECT_ROOT
        / "data_lake"
        / "gold"
        / "country_stats"
    )

    result.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {result.count():,}")
    print(f"Saved : {output}")

    return result