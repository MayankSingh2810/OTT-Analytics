import random

import pandas as pd

from faker import Faker

from config import RAW_DATA_DIR
from config import SEARCH_EVENTS

from utils.helpers import generate_search_id

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

behavior = pd.read_csv(
    RAW_DATA_DIR / "user_behavior.csv"
)

# ============================================================
# SEARCH VOCABULARY
# ============================================================

SEARCH_LIBRARY = {

    "Action":[
        "Action",
        "Fight",
        "War",
        "Mission",
        "John Wick",
        "Marvel",
        "Fast"
    ],

    "Comedy":[
        "Comedy",
        "Funny",
        "Stand Up",
        "Sitcom",
        "Family Comedy"
    ],

    "Drama":[
        "Drama",
        "Family",
        "Emotional",
        "Life Story"
    ],

    "Romance":[
        "Romantic",
        "Love",
        "Date Night",
        "Couple"
    ],

    "Sci-Fi":[
        "Space",
        "Sci-Fi",
        "Alien",
        "Time Travel",
        "Future"
    ],

    "Crime":[
        "Crime",
        "Detective",
        "Police",
        "Mafia",
        "Money Heist"
    ],

    "Thriller":[
        "Thriller",
        "Mystery",
        "Murder",
        "Suspense"
    ],

    "Horror":[
        "Ghost",
        "Haunted",
        "Zombie",
        "Horror"
    ],

    "Documentary":[
        "Nature",
        "History",
        "Wildlife",
        "Science"
    ]
}

# ============================================================
# GENERATE
# ============================================================

records = []

print("=" * 70)
print("GENERATING SEARCH HISTORY")
print("=" * 70)

for i in range(SEARCH_EVENTS):

    person = behavior.sample(1).iloc[0]

    user = person["user_id"]

    fav = person["favorite_genre_1"]

    if fav not in SEARCH_LIBRARY:
        fav = random.choice(list(SEARCH_LIBRARY.keys()))

    query = random.choice(
        SEARCH_LIBRARY[fav]
    )

    # 90% search success

    found = random.random() < 0.90

    if found:

        possible = content[
            content["genre"] == fav
        ]

        if len(possible):

            movie = possible.sample(1).iloc[0]

        else:

            movie = content.sample(1).iloc[0]

        clicked = movie["content_id"]

    else:

        clicked = None

    records.append({

        "search_id":generate_search_id(),

        "user_id":user,

        "search_time":fake.date_time_between(
            start_date="-365d",
            end_date="now"
        ),

        "search_query":query,

        "genre":fav,

        "result_found":"Yes" if found else "No",

        "clicked_content":clicked,

        "search_duration_sec":random.randint(3,45),

        "device":person["preferred_device"]

    })

    if (i+1)%50000==0:

        print(f"{i+1:,} searches generated...")

# ============================================================
# SAVE
# ============================================================

df = pd.DataFrame(records)

df.to_csv(

    RAW_DATA_DIR / "search_history.csv",

    index=False

)

print("="*70)

print(df.head())

print()

print(f"Rows : {len(df):,}")

print(f"Saved : {RAW_DATA_DIR/'search_history.csv'}")

print("="*70)