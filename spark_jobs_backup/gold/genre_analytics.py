"""
============================================================
Gold Layer
Genre Analytics
============================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc
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

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg("imdb_rating"),
                2
            ).alias("avg_imdb_rating")

        )

        .orderBy(
            desc("total_views")
        )

    )

    output = GOLD_DIR / "genre_analytics"

    genre.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {genre.count():,}")

    print(f"Saved : {output}")

    return genre