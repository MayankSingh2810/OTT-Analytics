"""
============================================================
Silver Layer
Users
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    current_date,
    year,
    to_date,
    greatest,
    lit
)

from config import BRONZE_DIR, SILVER_DIR


def transform_users(spark):

    print("=" * 70)
    print("Processing Users")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "users")
    )

    print(f"Original Rows : {df.count():,}")

    # -------------------------------------------------------
    # Remove duplicate users
    # -------------------------------------------------------

    df = df.dropDuplicates(["user_id"])

    # -------------------------------------------------------
    # Convert signup_date
    # -------------------------------------------------------

    df = df.withColumn(
        "signup_date",
        to_date(col("signup_date"))
    )

    # -------------------------------------------------------
    # Remove invalid ages
    # -------------------------------------------------------

    df = df.filter(
        col("age").isNotNull()
    )

    df = df.filter(
        (col("age") >= 13) &
        (col("age") <= 100)
    )

    # -------------------------------------------------------
    # Age Group
    # -------------------------------------------------------

    df = df.withColumn(

        "age_group",

        when(col("age") < 18, "Teen")
        .when(col("age") < 30, "Young Adult")
        .when(col("age") < 50, "Adult")
        .otherwise("Senior")

    )

    # -------------------------------------------------------
    # Membership Years
    # -------------------------------------------------------

    df = df.withColumn(

        "membership_years",

        greatest(

            year(current_date()) -
            year(col("signup_date")),

            lit(0)

        )

    )

    # -------------------------------------------------------
    # Sort
    # -------------------------------------------------------

    df = df.orderBy("user_id")

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "users"

    (
        df.write
        .mode("overwrite")
        .parquet(str(output))
    )

    print(f"Saved : {output}")

    return df