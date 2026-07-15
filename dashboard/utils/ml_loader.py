import json
from pathlib import Path

import pandas as pd


# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_MODELS = PROJECT_ROOT / "ml_models"


# =====================================================
# JSON LOADER
# =====================================================

def load_json(relative_path: str):

    path = ML_MODELS / relative_path

    if not path.exists():
        return {}

    with open(path, "r") as f:
        return json.load(f)


# =====================================================
# PARQUET LOADER
# =====================================================

def load_parquet(relative_path: str):

    path = ML_MODELS / relative_path

    if not path.exists():
        return pd.DataFrame()

    return pd.read_parquet(path)


# =====================================================
# RANDOM FOREST
# =====================================================

def load_random_forest_metrics():
    return load_json("random_forest/metrics.json")


# =====================================================
# GRADIENT BOOSTED
# =====================================================

def load_gradient_boosted_metrics():
    return load_json("gradient_boosted/metrics.json")


# =====================================================
# MODEL COMPARISON
# =====================================================

def load_model_comparison():
    return load_json("evaluation/model_comparison.json")


# =====================================================
# ARIMA FORECAST
# =====================================================

def load_forecast():
    return load_parquet("arima/forecast.parquet")

def load_als_recommendations(user_index=0, limit=10):

    from pathlib import Path
    import pandas as pd

    path = Path("../ml_models/als/recommendations")

    if not path.exists():
        path = Path("ml_models/als/recommendations")

    if not path.exists():
        return pd.DataFrame()

    try:

        df = pd.read_parquet(path)

        df = (
            df[df["userIndex"] == user_index]
            .sort_values(
                "PredictedRating",
                ascending=False
            )
            .head(limit)
        )

        return df

    except Exception:
        return pd.DataFrame()