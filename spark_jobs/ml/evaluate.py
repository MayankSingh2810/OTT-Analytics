import json
import os

# ==========================================================
# MODEL PATHS
# ==========================================================

RF_METRICS = "ml_models/random_forest/metrics.json"
GBT_METRICS = "ml_models/gradient_boosted/metrics.json"

# ==========================================================
# LOAD METRICS
# ==========================================================

with open(RF_METRICS) as f:
    rf = json.load(f)

with open(GBT_METRICS) as f:
    gbt = json.load(f)

# ==========================================================
# COMPARE
# ==========================================================

comparison = {

    "Random Forest": {

        "Algorithm": rf["algorithm"],

        "AUC": rf["auc"],

        "Training Rows": rf["training_rows"],

        "Testing Rows": rf["testing_rows"]

    },

    "Gradient Boosted Trees": {

        "Algorithm": gbt["algorithm"],

        "AUC": gbt["auc"],

        "Training Rows": gbt["training_rows"],

        "Testing Rows": gbt["testing_rows"]

    }

}

# ==========================================================
# BEST MODEL
# ==========================================================

if rf["auc"] >= gbt["auc"]:

    best = {

        "Best Model": "Random Forest",

        "Best AUC": rf["auc"],

        "Selection Reason": "Highest ROC-AUC"

    }

else:

    best = {

        "Best Model": "Gradient Boosted Trees",

        "Best AUC": gbt["auc"],

        "Selection Reason": "Highest ROC-AUC"

    }

comparison["Winner"] = best

# ==========================================================
# SAVE REPORT
# ==========================================================

os.makedirs(
    "ml_models/evaluation",
    exist_ok=True
)

with open(

    "ml_models/evaluation/model_comparison.json",

    "w"

) as f:

    json.dump(
        comparison,
        f,
        indent=4
    )

# ==========================================================
# PRINT
# ==========================================================

print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print()

print("Random Forest AUC        :", rf["auc"])

print("Gradient Boosted AUC     :", gbt["auc"])

print()

print("BEST MODEL :", best["Best Model"])
print("BEST AUC   :", best["Best AUC"])
print("REASON     :", best["Selection Reason"])

print()

print("Saved : ml_models/evaluation/model_comparison.json")
print("=" * 70)