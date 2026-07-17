"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
LIVE DASHBOARD GENERATOR
============================================================
"""

from pathlib import Path
from datetime import datetime
import random
import traceback

import pandas as pd

print("=" * 70)
print("STARTING LIVE DASHBOARD")
print("=" * 70)

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_PATH = PROJECT_ROOT / "data_lake" / "gold"

DASHBOARD_PATH = GOLD_PATH / "dashboard_summary"

LIVE_FOLDER = GOLD_PATH / "live_dashboard_summary"

LIVE_FOLDER.mkdir(parents=True, exist_ok=True)

LIVE_PATH = LIVE_FOLDER / "live_dashboard.parquet"

print("PROJECT ROOT :", PROJECT_ROOT)
print("GOLD PATH    :", GOLD_PATH)
print("SOURCE PATH  :", DASHBOARD_PATH)
print("OUTPUT PATH  :", LIVE_PATH)


# ==========================================================
# BUILD LIVE DASHBOARD
# ==========================================================

def build_live_dashboard():

    try:

        print("\nReading dashboard summary...")

        dashboard = pd.read_parquet(DASHBOARD_PATH)

        print("Dashboard Loaded")
        print(dashboard.head())

        row = dashboard.iloc[0]

        active_users = random.randint(1200, 8000)

        live_sessions = active_users + random.randint(500, 2500)

        watch_hours = round(
            float(row["watch_hours"]) + random.uniform(20, 400),
            2,
        )

        revenue_today = random.randint(25000, 120000)

        avg_completion = round(

            max(
                50,
                min(
                    98,
                    float(row["avg_completion"])
                    + random.uniform(-1.5, 1.5),
                ),
            ),

            2,

        )

        buffer_rate = round(
            random.uniform(0.5, 4.0),
            2,
        )

        like_rate = round(
            random.uniform(45, 70),
            2,
        )

        churn_risk = random.randint(150, 1200)

        live = pd.DataFrame(
            [
                {

                    "timestamp": datetime.now(),

                    "active_users": active_users,

                    "live_sessions": live_sessions,

                    "watch_hours": watch_hours,

                    "revenue_today": revenue_today,

                    "avg_completion": avg_completion,

                    "buffer_rate": buffer_rate,

                    "like_rate": like_rate,

                    "high_risk_users": churn_risk,

                    "registered_users": int(
                        row["registered_users"]
                    ),

                    "content_library": int(
                        row["content_library"]
                    ),

                }
            ]
        )

        print("\nGenerated Live Dashboard\n")
        print(live)

        live.to_parquet(
            LIVE_PATH,
            index=False,
        )

        print("\nSaved Successfully")

        print("=" * 70)
        print("LIVE DASHBOARD UPDATED")
        print("=" * 70)

    except Exception as e:

        print("\nERROR OCCURRED\n")

        traceback.print_exc()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    build_live_dashboard()