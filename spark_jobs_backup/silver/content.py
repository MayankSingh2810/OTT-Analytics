"""
============================================================
Silver Layer - Content
============================================================
"""

from pyspark.sql.functions import (
    col,
    when
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
    # Remove duplicates
    # -------------------------------------------------------

    df = df.dropDuplicates(["content_id"])

    # -------------------------------------------------------
    # IMDb Rating Category
    # -------------------------------------------------------

    df = df.withColumn(

        "rating_band",

        when(col("imdb_rating") >= 8, "Excellent")
        .when(col("imdb_rating") >= 6, "Good")
        .otherwise("Average")

    )

    # -------------------------------------------------------
    # Popularity Category
    # -------------------------------------------------------

    df = df.withColumn(

        "popularity_band",

        when(col("popularity_score") >= 80, "Trending")
        .when(col("popularity_score") >= 60, "Popular")
        .otherwise("Normal")

    )

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "content"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df