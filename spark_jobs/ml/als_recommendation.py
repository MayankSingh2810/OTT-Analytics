from pyspark.sql import SparkSession
from pyspark.sql.functions import dense_rank
from pyspark.sql.window import Window

from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS

# ==========================================================
# Spark
# ==========================================================

spark = (
    SparkSession.builder
    .appName("OTT Recommendation Engine")
    .getOrCreate()
)

# ==========================================================
# Load Gold Layer
# ==========================================================

df = spark.read.parquet(
    "data_lake/gold/top_content"
)

users = spark.read.parquet(
    "data_lake/gold/user_retention"
)

# ==========================================================
# Create Synthetic User-Content Interactions
# ==========================================================

interactions = (
    users.select("user_id")
    .crossJoin(
        df.select(
            "content_id",
            "imdb_rating"
        )
    )
)

# Keep dataset manageable

interactions = interactions.sample(0.02, seed=42)

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
    interactions.imdb_rating
)

# ==========================================================
# ALS
# ==========================================================

als = ALS(

    userCol="userIndex",

    itemCol="itemIndex",

    ratingCol="rating",

    coldStartStrategy="drop",

    nonnegative=True,

    rank=20,

    maxIter=10,

    regParam=0.1

)

model = als.fit(interactions)

# ==========================================================
# Recommendations
# ==========================================================

recommendations = model.recommendForAllUsers(10)

recommendations.write.mode("overwrite").parquet(
    "ml_models/als/recommendations"
)

model.write().overwrite().save(
    "ml_models/als/model"
)

print("=" * 60)
print("ALS Recommendation Engine Completed")
print("=" * 60)

spark.stop()