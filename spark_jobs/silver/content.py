"""
============================================================
Silver Layer
Content
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    round
)

from config import BRONZE_DIR, SILVER_DIR


def transform_content(spark):

    print("=" * 70)
    print("Processing Content")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "content")
    )

    print(f"Original Rows : {df.count():,}")

    # -------------------------------------------------------
    # Remove duplicate content
    # -------------------------------------------------------

    df = df.dropDuplicates(["content_id"])

    # -------------------------------------------------------
    # Remove invalid IMDb ratings
    # -------------------------------------------------------

    df = df.filter(
        (col("imdb_rating") >= 0) &
        (col("imdb_rating") <= 10)
    )

    # -------------------------------------------------------
    # Round important numeric columns
    # -------------------------------------------------------

    df = df.withColumn(
        "imdb_rating",
        round(col("imdb_rating"), 2)
    )

    df = df.withColumn(
        "popularity_score",
        round(col("popularity_score"), 2)
    )

    # -------------------------------------------------------
    # IMDb Rating Band
    # -------------------------------------------------------

    df = df.withColumn(

        "rating_band",

        when(col("imdb_rating") >= 8.5, "Excellent")
        .when(col("imdb_rating") >= 7.0, "Good")
        .when(col("imdb_rating") >= 5.0, "Average")
        .otherwise("Poor")

    )

    # -------------------------------------------------------
    # Popularity Band
    # -------------------------------------------------------

    df = df.withColumn(

        "popularity_band",

        when(col("popularity_score") >= 80, "Trending")
        .when(col("popularity_score") >= 60, "Popular")
        .when(col("popularity_score") >= 40, "Moderate")
        .otherwise("Low")

    )

    # -------------------------------------------------------
    # Sort
    # -------------------------------------------------------

    df = df.orderBy("content_id")

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "content"

    (
        df.write
        .mode("overwrite")
        .parquet(str(output))
    )

    print(f"Saved : {output}")

    return df