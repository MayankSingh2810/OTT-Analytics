"""
============================================================
Silver Layer - Search History
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    lower,
    trim
)

from config import BRONZE_DIR, SILVER_DIR


def transform_search_history(spark):

    print("=" * 70)
    print("Processing Search History")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "search_history")
    )

    print(f"Original Rows : {df.count():,}")

    # -------------------------------------------------------
    # Remove duplicate searches
    # -------------------------------------------------------

    df = df.dropDuplicates(["search_id"])

    # -------------------------------------------------------
    # Clean Search Query
    # -------------------------------------------------------

    df = df.withColumn(
        "search_query",
        lower(trim(col("search_query")))
    )

    # -------------------------------------------------------
    # Search Success
    # -------------------------------------------------------

    df = df.withColumn(

        "search_success",

        when(
            col("result_found") == "Yes",
            "Yes"
        ).otherwise("No")

    )

    # -------------------------------------------------------
    # Search Duration Category
    # -------------------------------------------------------

    df = df.withColumn(

        "search_speed",

        when(col("search_duration_sec") <= 3, "Fast")
        .when(col("search_duration_sec") <= 8, "Normal")
        .otherwise("Slow")

    )

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "search_history"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df