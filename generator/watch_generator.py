import random

import pandas as pd
from faker import Faker

from config import RAW_DATA_DIR
from config import WATCH_EVENTS

from utils.helpers import generate_watch_id

from generator.behavior_engine import (
    assign_profile,
    get_profile,
)

fake = Faker()

# ==========================================================
# LOAD DATA
# ==========================================================

users = pd.read_csv(RAW_DATA_DIR / "users.csv")

content = pd.read_csv(RAW_DATA_DIR / "content.csv")

subscriptions = pd.read_csv(RAW_DATA_DIR / "subscriptions.csv")

# ==========================================================
# CONSTANTS
# ==========================================================

NETWORKS = [
    "WiFi",
    "4G",
    "5G"
]

SOURCES = [
    "Home",
    "Search",
    "Recommendation",
    "Trending",
    "Continue Watching"
]

records = []

print("=" * 70)
print("GENERATING WATCH HISTORY")
print("=" * 70)

# ==========================================================
# GENERATE EVENTS
# ==========================================================

for i in range(WATCH_EVENTS):

    # Random User
    user = users.sample(n=1).iloc[0]

    # Behaviour Profile
    profile_name = assign_profile()
    profile = get_profile(profile_name)

    # Preferred Genre
    preferred_genre = random.choice(profile["preferred_genres"])

    filtered = content[
        content["genre"] == preferred_genre
    ]

    if len(filtered) > 0:
        movie = filtered.sample(n=1).iloc[0]
    else:
        movie = content.sample(n=1).iloc[0]

    runtime = movie["duration_minutes"]

    completion = random.randint(
        profile["completion_range"][0],
        profile["completion_range"][1]
    )

    watch_minutes = round(
        runtime * completion / 100,
        2
    )

    device = random.choice(
        profile["preferred_devices"]
    )

    network = random.choice(NETWORKS)

    source = random.choice(SOURCES)

    start_time = fake.date_time_between(
        start_date="-365d",
        end_date="now"
    )

    end_time = start_time + pd.Timedelta(
        minutes=watch_minutes
    )

    records.append({

        "watch_id": generate_watch_id(),

        "user_id": user["user_id"],

        "content_id": movie["content_id"],

        "watch_start": start_time,

        "watch_end": end_time,

        "watch_minutes": watch_minutes,

        "completion_pct": completion,

        "device": device,

        "network": network,

        "recommendation_source": source,

        "liked": random.choice(
            ["Yes", "No"]
        ),

        "added_to_watchlist": random.choice(
            ["Yes", "No"]
        )

    })

    if (i + 1) % 25000 == 0:

        print(f"{i+1:,} watch events generated...")

# ==========================================================
# SAVE DATASET
# ==========================================================

df = pd.DataFrame(records)

output = RAW_DATA_DIR / "watch_history.csv"

df.to_csv(
    output,
    index=False
)

print("\n")
print("=" * 70)
print("WATCH HISTORY GENERATED")
print("=" * 70)

print(df.head())

print("=" * 70)

print(f"Rows Generated : {len(df):,}")

print(f"Columns : {len(df.columns)}")

print(f"Output : {output}")

print(f"Duplicate watch_id : {df['watch_id'].duplicated().sum()}")

print("\nNull Values")

print(df.isnull().sum())

print("=" * 70)

print("Generation Complete")

print("=" * 70)