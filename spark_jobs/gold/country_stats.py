from pathlib import Path

from pyspark.sql.functions import (
    avg,
    count,
    countDistinct,
    col,
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

    users = spark.read.parquet(
        str(PROJECT_ROOT / "data_lake/silver/users")
    )

    # Bring in country via user_id, since watch_history has no country column
    watch = watch.join(
        users.select("user_id", "country"),
        "user_id",
        "left"
    )

    result = (
        watch
        .groupBy("country")
        .agg(
            count("*").alias("views"),
            countDistinct("user_id").alias("unique_users"),
            round(avg("watch_minutes"), 2).alias("avg_watch_minutes"),
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