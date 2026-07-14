from pathlib import Path

from pyspark.sql.functions import (
    avg,
    count,
    col,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_country_stats(spark):

    print("Building country_stats...")

    silver = (
        PROJECT_ROOT
        / "data_lake"
        / "silver"
        / "live_events"
    )

    df = spark.read.parquet(str(silver))

    result = (
        df.groupBy("country")
        .agg(
            count("*").alias("total_events"),
            avg("watch_time_seconds").alias("avg_watch_seconds"),
            avg("buffer_time_ms").alias("avg_buffer_ms")
        )
        .orderBy(col("total_events").desc())
    )

    output = (
        PROJECT_ROOT
        / "data_lake"
        / "gold"
        / "country_stats"
    )

    result.write.mode("overwrite").parquet(str(output))

    print("✓ country_stats completed")