"""
============================================================
Gold Layer
Genre Analytics
Enterprise Version
============================================================
"""

from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    desc,
    sum
)

from config import SILVER_DIR, GOLD_DIR


def build_genre_analytics(spark):

    print("=" * 70)
    print("Building Genre Analytics")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    genre = (

        watch

        .join(
            content,
            "content_id"
        )

        .groupBy("genre")

        .agg(

            count("*").alias("total_views"),

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
                avg("imdb_rating"),
                2
            ).alias("avg_imdb_rating"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("total_watch_hours")

        )

        .orderBy(
            desc("total_views")
        )

    )

    output = GOLD_DIR / "genre_analytics"

    genre.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {genre.count():,}")
    print(f"Saved : {output}")

    return genre