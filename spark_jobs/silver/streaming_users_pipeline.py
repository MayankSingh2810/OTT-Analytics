from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    to_date
)

# =====================================================
# Spark Session
# =====================================================

spark = (
    SparkSession.builder
    .appName("OTT Silver User Streaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 60)
print("OTT SILVER USER STREAMING STARTED")
print("=" * 60)

# =====================================================
# Infer Bronze Schema
# =====================================================

bronze_schema = (
    spark.read
    .parquet("data_lake/bronze/live_users")
    .schema
)

print("Bronze User schema loaded.")

# =====================================================
# Read Bronze Stream
# =====================================================

bronze_df = (
    spark.readStream
    .schema(bronze_schema)
    .parquet("data_lake/bronze/live_users")
)

# =====================================================
# Cleaning
# =====================================================

silver_df = (

    bronze_df

    .dropDuplicates(["user_id"])

    .filter(col("user_id").isNotNull())

    .filter(col("email").isNotNull())

    .withColumn(
        "country",
        trim(col("country"))
    )

    .withColumn(
        "city",
        trim(col("city"))
    )

    .withColumn(
        "preferred_language",
        trim(col("preferred_language"))
    )

    .withColumn(
        "preferred_genre",
        trim(col("preferred_genre"))
    )

    .withColumn(
        "account_status",
        upper(trim(col("account_status")))
    )

    .withColumn(
        "signup_date",
        to_date(col("signup_date"))
    )

)

# =====================================================
# Write Silver
# =====================================================

query = (

    silver_df.writeStream

    .format("parquet")

    .outputMode("append")

    .option(
        "checkpointLocation",
        "data_lake/checkpoints/silver_users"
    )

    .start("data_lake/silver/live_users")

)

print("\nSilver User Stream Running...\n")

query.awaitTermination()