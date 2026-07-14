"""
============================================================
Silver Layer - Ratings
============================================================
"""

from pyspark.sql.functions import (
    col,
    when
)

from config import BRONZE_DIR, SILVER_DIR


def transform_ratings(spark):

    print("=" * 70)
    print("Processing Ratings")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "ratings")
    )

    print(f"Original Rows : {df.count():,}")

    # -------------------------------------------------------
    # Remove duplicate ratings
    # -------------------------------------------------------

    df = df.dropDuplicates(["rating_id"])

    # -------------------------------------------------------
    # Keep only valid ratings
    # -------------------------------------------------------

    df = df.filter(
        (col("rating") >= 1) &
        (col("rating") <= 5)
    )

    # -------------------------------------------------------
    # Rating Category
    # -------------------------------------------------------

    df = df.withColumn(

        "rating_category",

        when(col("rating") >= 4, "Positive")
        .when(col("rating") == 3, "Neutral")
        .otherwise("Negative")

    )

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "ratings"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df