import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# ==========================================================
# MYSQL CONFIGURATION
# ==========================================================

MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "ott_analytics"

# ==========================================================
# SQLALCHEMY ENGINE
# ==========================================================

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ==========================================================
# MYSQL TABLE MAPPING
# ==========================================================

TABLES = {

    "dashboard": "dashboard_summary",

    "daily_users": "daily_active_users",

    "monthly_users": "monthly_active_users",

    "retention": "user_retention",

    "watch_time": "watch_time_summary",

    "genre": "genre_stats",

    "genre_analytics": "genre_analytics",

    "top_content": "top_content",

    "content": "content_performance",

    "country": "country_stats",

    "device": "device_stats",

    "hourly": "hourly_usage",

    "quality": "quality_stats",

    "subscription": "subscription_stats",

    "subscription_revenue": "subscription_revenue",

    "network": "network_stats",

    "popular": "popular_content",

    "events": "event_stats",

    "churn": "churn_features"

}

# ==========================================================
# LOAD TABLE
# ==========================================================

@st.cache_data(ttl=10)
def load_table(name: str):

    if name not in TABLES:
        return pd.DataFrame()

    try:

        df = pd.read_sql(
            f"SELECT * FROM {TABLES[name]}",
            engine
        )

        # ---------------- Dashboard aliases ----------------

        if name == "dashboard":

            if "avg_watch_seconds" in df.columns:
                df["watch_hours"] = (
                    pd.to_numeric(df["avg_watch_seconds"], errors="coerce")
                    / 3600
                )

            if "unique_users" in df.columns:
                df["registered_users"] = pd.to_numeric(
                    df["unique_users"],
                    errors="coerce"
                )

            if "unique_content" in df.columns:
                df["content_library"] = pd.to_numeric(
                    df["unique_content"],
                    errors="coerce"
                )

            if "avg_completion" in df.columns:
                df["avg_completion"] = pd.to_numeric(
                    df["avg_completion"],
                    errors="coerce"
                )

        return df

    except Exception as e:

        st.error(f"MySQL Error : {e}")

        return pd.DataFrame()