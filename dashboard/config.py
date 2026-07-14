"""
==========================================================
OTT Stream Intelligence
Dashboard Configuration
==========================================================
"""

from pathlib import Path

# ==========================================================
# PROJECT
# ==========================================================

DASHBOARD_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = DASHBOARD_DIR.parent

# ==========================================================
# DATA LAKE
# ==========================================================

DATA_LAKE = PROJECT_ROOT / "data_lake"

GOLD_DIR = DATA_LAKE / "gold"

# ==========================================================
# STREAMLIT
# ==========================================================

APP_TITLE = "OTT Stream Intelligence"

REFRESH_SECONDS = 10

# ==========================================================
# GOLD TABLES
# ==========================================================

TABLES = {

    "dashboard": GOLD_DIR / "dashboard_summary",

    "daily_users": GOLD_DIR / "daily_active_users",

    "monthly_users": GOLD_DIR / "monthly_active_users",

    "retention": GOLD_DIR / "user_retention",

    "watch_time": GOLD_DIR / "watch_time_summary",

    "genre": GOLD_DIR / "genre_analytics",

    "top_content": GOLD_DIR / "top_content",

    "content": GOLD_DIR / "content_performance",

    "country": GOLD_DIR / "country_stats",

    "device": GOLD_DIR / "device_stats",

    "hourly": GOLD_DIR / "hourly_usage",

    "quality": GOLD_DIR / "quality_stats",

    "revenue": GOLD_DIR / "subscription_revenue",

    "churn": GOLD_DIR / "churn_features"

}