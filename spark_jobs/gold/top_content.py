"""
==========================================================
Gold Layer
Top Content
Enterprise Version
==========================================================
"""

from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    desc,
    sum,
    when,
    col
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

        .join(
            content,
            "content_id"
        )

        .groupBy(
            "content_id",
            "title",
            "genre",
            "content_type"
        )

        .agg(

            count("*").alias("views"),

            countDistinct("user_id").alias("unique_viewers"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg(
                    when(col("liked") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("like_rate"),

            round(
                avg(
                    when(col("completed") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("completion_rate"),

            round(
                avg(
                    when(col("binge_watch") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("binge_watch_rate"),

            round(
                avg("imdb_rating"),
                2
            ).alias("imdb_rating"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("watch_hours")

        )

        .orderBy(
            desc("views")
        )

    )

    output = GOLD_DIR / "top_content"

    top.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {top.count():,}")
    print(f"Saved : {output}")

    return top