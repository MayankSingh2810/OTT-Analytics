from pyspark.sql import SparkSession

from pyspark.ml.feature import VectorAssembler

from pyspark.ml.classification import GBTClassifier

from pyspark.ml.evaluation import BinaryClassificationEvaluator

import json
import os

# ==========================================================
# Spark Session
# ==========================================================

spark = (
    SparkSession.builder
    .appName("OTT Gradient Boosted Trees")
    .getOrCreate()
)

# ==========================================================
# Load Feature Store
# ==========================================================

df = spark.read.parquet(
    "data_lake/feature_store/churn_training"
)

feature_columns = [

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

    "age_group_index"

]

assembler = VectorAssembler(

    inputCols=feature_columns,

    outputCol="features"

)

dataset = assembler.transform(df)

train, test = dataset.randomSplit([0.8, 0.2], seed=42)

# ==========================================================
# Gradient Boosted Trees
# ==========================================================

gbt = GBTClassifier(

    labelCol="label",

    featuresCol="features",

    maxIter=100,

    maxDepth=6,

    seed=42

)

model = gbt.fit(train)

predictions = model.transform(test)

# ==========================================================
# Evaluate
# ==========================================================

evaluator = BinaryClassificationEvaluator(
    labelCol="label"
)

auc = evaluator.evaluate(predictions)

print("=" * 60)
print("Gradient Boosted Trees AUC :", auc)
print("=" * 60)

# ==========================================================
# Feature Importance
# ==========================================================

print("\nFeature Importance")

for feature, importance in zip(feature_columns, model.featureImportances):
    print(f"{feature:25} {importance:.4f}")

# ==========================================================
# Ensure Output Directory Exists
# ==========================================================

os.makedirs("ml_models/gradient_boosted", exist_ok=True)

# ==========================================================
# Save Model
# ==========================================================

model_path = "ml_models/gradient_boosted/model"

model.write().overwrite().save(model_path)

# ==========================================================
# Save Predictions
# ==========================================================

predictions.select(
    "user_id",
    "label",
    "prediction",
    "probability"
).write.mode("overwrite").parquet(
    "ml_models/gradient_boosted/predictions"
)

# ==========================================================
# Save Metrics
# ==========================================================

metrics = {

    "algorithm": "Spark MLlib Gradient Boosted Trees",

    "iterations": 100,

    "max_depth": 6,

    "auc": float(auc),

    "training_rows": train.count(),

    "testing_rows": test.count()

}

with open(
    "ml_models/gradient_boosted/metrics.json",
    "w"
) as f:

    json.dump(metrics, f, indent=4)

# ==========================================================
# Save Feature Importance
# ==========================================================

feature_importance = {
    feature: float(importance)
    for feature, importance in zip(
        feature_columns,
        model.featureImportances
    )
}

with open(
    "ml_models/gradient_boosted/feature_importance.json",
    "w"
) as f:
    json.dump(feature_importance, f, indent=4)

print("GBT Model Saved Successfully")

spark.stop()