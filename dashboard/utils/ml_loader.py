import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ML_MODELS = PROJECT_ROOT / "ml_models"


def load_json(relative_path: str):

    path = ML_MODELS / relative_path

    if not path.exists():
        return {}

    with open(path, "r") as f:
        return json.load(f)


def load_parquet(relative_path: str):

    path = ML_MODELS / relative_path

    if not path.exists():
        return pd.DataFrame()

    return pd.read_parquet(path)


def load_random_forest_metrics():
    return load_json("random_forest/metrics.json")


def load_gradient_boosted_metrics():
    return load_json("gradient_boosted/metrics.json")


def load_model_comparison():
    return load_json("evaluation/model_comparison.json")


def load_forecast():
    return load_parquet("arima/forecast.parquet")


def load_als_recommendations(limit=10):

    path = ML_MODELS / "als" / "recommendations"

    if not path.exists():
        return pd.DataFrame()

    try:

        df = pd.read_parquet(path)

        df = (
            df.sort_values(
                "PredictedRating",
                ascending=False
            )
            .head(limit)
        )

        return df

    except Exception as e:
        print(e)
        return pd.DataFrame()