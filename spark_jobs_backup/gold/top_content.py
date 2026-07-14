"""
============================================================
Gold Layer
Top Content Analytics
============================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc
)

from config import SILVER_DIR, GOLD_DIR


def build_top_content(spark):

    print("=" * 70)
    print("Building Top Content")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    top = (

        watch

        .groupBy("content_id")

        .agg(

            count("*").alias("total_views"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion")

        )

        .join(
            content,
            "content_id"
        )

        .orderBy(
            desc("total_views")
        )

    )

    output = GOLD_DIR / "top_content"

    top.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {top.count():,}")
    print(f"Saved : {output}")

    return top