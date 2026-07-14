import random
import pandas as pd

from config import RAW_DATA_DIR, TOTAL_CONTENT
from utils.helpers import generate_content_id

# ==========================================================
# MASTER DATA
# ==========================================================

GENRES = [
    "Action",
    "Drama",
    "Comedy",
    "Sci-Fi",
    "Thriller",
    "Romance",
    "Crime",
    "Fantasy",
    "Horror",
    "Documentary"
]

LANGUAGES = [
    "English",
    "Hindi",
    "Spanish",
    "French",
    "Japanese",
    "Korean"
]

COUNTRIES = [
    "USA",
    "India",
    "UK",
    "Canada",
    "France",
    "Japan",
    "South Korea"
]

PRODUCTION_HOUSES = [
    "Netflix Studios",
    "Marvel",
    "Warner Bros",
    "Disney",
    "Sony",
    "Universal",
    "Prime Originals",
    "Paramount"
]

AGE_RATINGS = [
    "U",
    "U/A",
    "A"
]

CONTENT_TYPES = [
    "Movie",
    "Series"
]

ADJECTIVES = [
    "Dark",
    "Silent",
    "Hidden",
    "Lost",
    "Golden",
    "Broken",
    "Infinite",
    "Last",
    "Secret",
    "Crimson"
]

NOUNS = [
    "Empire",
    "Shadow",
    "Dream",
    "Kingdom",
    "Mission",
    "Journey",
    "Code",
    "Planet",
    "Legacy",
    "Storm"
]

# ==========================================================

records = []

for _ in range(TOTAL_CONTENT):

    title = f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)}"

    records.append({

        "content_id": generate_content_id(),

        "title": title,

        "content_type": random.choice(CONTENT_TYPES),

        "genre": random.choice(GENRES),

        "language": random.choice(LANGUAGES),

        "release_year": random.randint(1995, 2026),

        "duration_minutes": random.randint(70, 180),

        "age_rating": random.choice(AGE_RATINGS),

        "imdb_rating": round(random.uniform(5.5, 9.8),1),

        "popularity_score": round(random.uniform(40,100),2),

        "production_house": random.choice(PRODUCTION_HOUSES),

        "country": random.choice(COUNTRIES),

        "license_cost": round(random.uniform(50000,10000000),2)

    })

df = pd.DataFrame(records)

output = RAW_DATA_DIR / "content.csv"

df.to_csv(output,index=False)

print("="*60)
print("CONTENT DATA GENERATED")
print(df.head())
print("="*60)
print(f"Rows : {len(df)}")
print(f"Saved : {output}")