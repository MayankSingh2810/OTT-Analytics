from pyspark.sql import SparkSession
from pyspark.sql.functions import rand
from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS

# ==========================================================
# Spark Session
# ==========================================================

spark = (
    SparkSession.builder
    .appName("OTT Recommendation Engine")
    .getOrCreate()
)

# ==========================================================
# Load Gold Layer
# ==========================================================

content = spark.read.parquet(
    "data_lake/gold/top_content"
)

users = spark.read.parquet(
    "data_lake/gold/user_retention"
)

# ==========================================================
# Synthetic User–Movie Interactions
# ==========================================================

interactions = (
    users.select("user_id")
    .crossJoin(
        content.select(
            "content_id",
            "title",
            "genre",
            "imdb_rating"
        )
    )
)

# keep dataset manageable

interactions = (
    interactions
    .sample(0.02, seed=42)
)

# ==========================================================
# Encode IDs
# ==========================================================

user_indexer = StringIndexer(
    inputCol="user_id",
    outputCol="userIndex"
)

item_indexer = StringIndexer(
    inputCol="content_id",
    outputCol="itemIndex"
)

interactions = user_indexer.fit(interactions).transform(interactions)
interactions = item_indexer.fit(interactions).transform(interactions)

# ==========================================================
# Rating
# ==========================================================

interactions = interactions.withColumn(
    "rating",
    interactions.imdb_rating + rand(seed=42)
)

# ==========================================================
# Train ALS
# ==========================================================

als = ALS(
    userCol="userIndex",
    itemCol="itemIndex",
    ratingCol="rating",
    rank=20,
    maxIter=10,
    regParam=0.1,
    coldStartStrategy="drop",
    nonnegative=True
)

model = als.fit(interactions)

# ==========================================================
# Recommendations
# ==========================================================

recommendations = model.recommendForAllUsers(10)

# ==========================================================
# Item Mapping
# ==========================================================

item_mapping = (
    interactions
    .select(
        "itemIndex",
        "content_id",
        "title",
        "genre"
    )
    .dropDuplicates(["itemIndex"])
)

# ==========================================================
# Explode Recommendations
# ==========================================================

from pyspark.sql.functions import explode

recommendations = recommendations.withColumn(
    "recommendation",
    explode("recommendations")
)

recommendations = recommendations.select(
    "userIndex",
    recommendations.recommendation.itemIndex.alias("itemIndex"),
    recommendations.recommendation.rating.alias("PredictedRating")
)

# ==========================================================
# Join Movie Information
# ==========================================================

recommendations = (
    recommendations
    .join(
        item_mapping,
        on="itemIndex",
        how="left"
    )
)

# ==========================================================
# Save Recommendations
# ==========================================================

recommendations.write.mode("overwrite").parquet(
    "ml_models/als/recommendations"
)

model.write().overwrite().save(
    "ml_models/als/model"
)

print("=" * 70)
print("ALS Recommendation Engine Completed Successfully")
print("=" * 70)

spark.stop()