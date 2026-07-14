from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD = PROJECT_ROOT / "data_lake" / "gold"


@st.cache_data
def load_table(folder):

    path = GOLD / folder

    files = list(path.glob("*.parquet"))

    if len(files) == 0:
        raise Exception(f"{folder} not found")

    dfs = [pd.read_parquet(f) for f in files]

    return pd.concat(dfs, ignore_index=True)


# ----------------------------
# Executive Dashboard
# ----------------------------

def load_dashboard_summary():
    return load_table("dashboard_summary")


def load_device():
    return load_table("device_stats")


def load_country():
    return load_table("country_stats")


def load_genre():
    return load_table("genre_stats")


def load_subscription():
    return load_table("subscription_stats")


def load_events():
    return load_table("event_stats")


def load_quality():
    return load_table("quality_stats")


def load_network():
    return load_table("network_stats")


def load_content():
    return load_table("popular_content")


def load_hourly():
    return load_table("hourly_usage")