import random

import pandas as pd

from faker import Faker

from config import RAW_DATA_DIR
from config import TOTAL_RATINGS

from utils.helpers import generate_rating_id

fake = Faker()

# ============================================================
# LOAD DATA
# ============================================================

users = pd.read_csv(
    RAW_DATA_DIR / "users.csv"
)

content = pd.read_csv(
    RAW_DATA_DIR / "content.csv"
)

# ============================================================
# GENERATE RATINGS
# ============================================================

records = []

print("=" * 70)
print("GENERATING RATINGS")
print("=" * 70)

for i in range(TOTAL_RATINGS):

    user = users.sample(1).iloc[0]

    movie = content.sample(1).iloc[0]

    imdb = float(movie["imdb_rating"])

    # ---------------------------------------
    # Rating follows IMDb score
    # ---------------------------------------

    if imdb >= 8.5:
        rating = random.choice([5, 5, 5, 4])
    elif imdb >= 7.5:
        rating = random.choice([5, 4, 4, 3])
    elif imdb >= 6.5:
        rating = random.choice([4, 3, 3, 2])
    else:
        rating = random.choice([3, 2, 2, 1])

    # ---------------------------------------
    # Recommendation
    # ---------------------------------------

    would_recommend = "Yes" if rating >= 4 else "No"

    # ---------------------------------------
    # Watch Completion
    # ---------------------------------------

    watch_completed = random.choice(
        ["Yes", "No"]
    )

    # ---------------------------------------
    # Sentiment
    # ---------------------------------------

    if rating >= 4:
        sentiment = "Positive"
    elif rating == 3:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"

    records.append({

        "rating_id": generate_rating_id(),

        "user_id": user["user_id"],

        "content_id": movie["content_id"],

        "rating": rating,

        "review_date": fake.date_between(
            start_date="-365d",
            end_date="today"
        ),

        "watch_completed": watch_completed,

        "would_recommend": would_recommend,

        "sentiment": sentiment

    })

    if (i + 1) % 50000 == 0:

        print(f"{i + 1:,} ratings generated...")

# ============================================================
# SAVE
# ============================================================

ratings = pd.DataFrame(records)

ratings.to_csv(
    RAW_DATA_DIR / "ratings.csv",
    index=False
)

print("=" * 70)
print(ratings.head())

print(f"\nRows : {len(ratings):,}")

print(f"Saved : {RAW_DATA_DIR / 'ratings.csv'}")

print("=" * 70)