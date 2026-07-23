from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import StringIndexer

# ==========================================================
# Spark Session
# ==========================================================

spark = (
    SparkSession.builder
    .appName("OTT Feature Store")
    .getOrCreate()
)

# ==========================================================
# Load Gold Layer
# ==========================================================

df = spark.read.parquet(
    "data_lake/gold/user_retention"
)

print(f"Loaded {df.count()} users")

# ==========================================================
# Create Churn Label (composite score, not a single-feature rule)
# ==========================================================

df = df.withColumn(
    "churn_score",
    (
        when(col("days_inactive") > 45, 1).otherwise(0)
        +
        when(col("avg_completion") < 50, 1).otherwise(0)
        +
        when(col("avg_watch_minutes") < 60, 1).otherwise(0)
        +
        when(col("total_sessions") < 5, 1).otherwise(0)
        +
        when(col("account_status") == "Inactive", 1).otherwise(0)
    )
)

df = df.withColumn(
    "label",
    when(col("churn_score") >= 3, 1).otherwise(0)
).drop("churn_score")

# ==========================================================
# Encode Categorical Features
# ==========================================================

categorical_columns = [
    "gender",
    "country",
    "preferred_genre",
    "device_type",
    "profile_type",
    "age_group"
]

for column in categorical_columns:

    indexer = StringIndexer(
        inputCol=column,
        outputCol=f"{column}_index",
        handleInvalid="keep"
    )

    df = indexer.fit(df).transform(df)

# ==========================================================
# Select ML Features
# ==========================================================

feature_store = df.select(

    "user_id",

    "total_sessions",

    "avg_watch_minutes",

    "avg_completion",

    "days_inactive",

    "age",

    "membership_years",

    "gender_index",

    "country_index",

    "preferred_genre_index",

    "device_type_index",

    "profile_type_index",

    "age_group_index",

    "label"

)

# ==========================================================
# Save Feature Store
# ==========================================================

output = "data_lake/feature_store/churn_training"

(
    feature_store
    .coalesce(1)
    .write
    .mode("overwrite")
    .parquet(output)
)

print("=" * 60)
print("FEATURE STORE CREATED")
print("=" * 60)
print(f"Rows : {feature_store.count()}")
print(f"Saved : {output}")

spark.stop()