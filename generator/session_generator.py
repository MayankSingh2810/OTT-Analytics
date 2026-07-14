import random

import pandas as pd

from faker import Faker

from config import RAW_DATA_DIR
from config import SESSION_EVENTS

from utils.helpers import generate_session_id

fake = Faker()

# ============================================================
# LOAD DATA
# ============================================================

users = pd.read_csv(
    RAW_DATA_DIR / "users.csv"
)

behavior = pd.read_csv(
    RAW_DATA_DIR / "user_behavior.csv"
)

# ============================================================
# DEVICES
# ============================================================

NETWORKS = [
    "WiFi",
    "4G",
    "5G"
]

APP_VERSION = [
    "3.1.0",
    "3.2.1",
    "3.3.0",
    "4.0.0"
]

OS = [
    "Android",
    "iOS",
    "Windows",
    "macOS",
    "Android TV"
]

records = []

print("=" * 70)
print("GENERATING USER SESSIONS")
print("=" * 70)

for i in range(SESSION_EVENTS):

    person = behavior.sample(1).iloc[0]

    login = fake.date_time_between(
        start_date="-365d",
        end_date="now"
    )

    duration = random.randint(2, 240)

    logout = login + pd.Timedelta(minutes=duration)

    records.append({

        "session_id": generate_session_id(),

        "user_id": person["user_id"],

        "login_time": login,

        "logout_time": logout,

        "session_minutes": duration,

        "device": person["preferred_device"],

        "operating_system": random.choice(OS),

        "network": random.choice(NETWORKS),

        "app_version": random.choice(APP_VERSION),

        "location": fake.city(),

        "crashed": random.choices(
            ["Yes", "No"],
            weights=[2, 98]
        )[0]

    })

    if (i + 1) % 50000 == 0:
        print(f"{i+1:,} sessions generated...")

# ============================================================
# SAVE
# ============================================================

df = pd.DataFrame(records)

df.to_csv(
    RAW_DATA_DIR / "sessions.csv",
    index=False
)

print("=" * 70)
print(df.head())
print()
print(f"Rows : {len(df):,}")
print(f"Saved : {RAW_DATA_DIR/'sessions.csv'}")
print("=" * 70)