import random

import pandas as pd

from config import RAW_DATA_DIR

from generator.behavior_engine import (
    assign_profile,
    get_profile,
)

# ==========================================================
# LOAD USERS
# ==========================================================

users = pd.read_csv(
    RAW_DATA_DIR / "users.csv"
)

records = []

print("=" * 70)
print("GENERATING USER BEHAVIOUR PROFILES")
print("=" * 70)

# ==========================================================
# BUILD PROFILE FOR EACH USER
# ==========================================================

for _, user in users.iterrows():

    profile_name = assign_profile()

    profile = get_profile(profile_name)

    genres = random.sample(
        profile["preferred_genres"],
        k=min(2, len(profile["preferred_genres"]))
    )

    records.append({

        "user_id": user["user_id"],

        "profile": profile_name,

        "preferred_device": random.choice(
            profile["preferred_devices"]
        ),

        "favorite_genre_1": genres[0],

        "favorite_genre_2": genres[1] if len(genres) > 1 else genres[0],

        "avg_completion_pct": random.randint(
            profile["completion_range"][0],
            profile["completion_range"][1]
        ),

        "monthly_watch_target": random.randint(
            profile["monthly_watch_range"][0],
            profile["monthly_watch_range"][1]
        ),

        "binge_score": random.randint(30,100)

    })

# ==========================================================
# SAVE CSV
# ==========================================================

df = pd.DataFrame(records)

output = RAW_DATA_DIR / "user_behavior.csv"

df.to_csv(
    output,
    index=False
)

print(df.head())

print()

print(f"Profiles Generated : {len(df):,}")

print(f"Output : {output}")

print("=" * 70)