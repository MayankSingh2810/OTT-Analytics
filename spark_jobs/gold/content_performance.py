"""
==========================================================
Gold Layer
Content Performance
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


def build_content_performance(spark):

    print("=" * 70)
    print("Building Content Performance")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    performance = (

        watch

        .join(
            content,
            "content_id"
        )

        .groupBy(

            "content_id",
            "title",
            "genre"

        )

        .agg(

            count("*").alias("views"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg("imdb_rating"),
                2
            ).alias("avg_rating")

        )

        .orderBy(
            desc("views")
        )

    )

    output = GOLD_DIR / "content_performance"

    performance.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {performance.count():,}")

    print(f"Saved : {output}")

    return performance