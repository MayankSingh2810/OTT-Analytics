import random
import pandas as pd
from faker import Faker

from config import RAW_DATA_DIR, TOTAL_USERS
from utils.helpers import generate_user_id

fake = Faker()

# ==========================================================
# MASTER DATA
# ==========================================================

COUNTRIES = [
    "India",
    "USA",
    "Canada",
    "UK",
    "Australia"
]

CITIES = {
    "India": [
        "Delhi",
        "Mumbai",
        "Bangalore",
        "Hyderabad",
        "Pune"
    ],
    "USA": [
        "New York",
        "Chicago",
        "Seattle",
        "Los Angeles"
    ],
    "Canada": [
        "Toronto",
        "Ottawa",
        "Vancouver"
    ],
    "UK": [
        "London",
        "Manchester",
        "Liverpool"
    ],
    "Australia": [
        "Sydney",
        "Melbourne",
        "Perth"
    ]
}

GENRES = [
    "Action",
    "Drama",
    "Comedy",
    "Thriller",
    "Sci-Fi",
    "Romance",
    "Crime"
]

LANGUAGES = [
    "English",
    "Hindi",
    "Spanish"
]

DEVICES = [
    "Mobile",
    "TV",
    "Tablet",
    "Laptop"
]

PROFILES = [
    "Single",
    "Family",
    "Kids"
]

ACCOUNT_STATUS = [
    "Active",
    "Inactive"
]

# ==========================================================

records = []

for _ in range(TOTAL_USERS):

    country = random.choice(COUNTRIES)

    city = random.choice(CITIES[country])

    records.append({

        "user_id": generate_user_id(),

        "first_name": fake.first_name(),

        "last_name": fake.last_name(),

        "email": fake.unique.email(),

        "gender": random.choice([
            "Male",
            "Female"
        ]),

        "age": random.randint(18,75),

        "country": country,

        "city": city,

        "preferred_language": random.choice(LANGUAGES),

        "preferred_genre": random.choice(GENRES),

        "device_type": random.choice(DEVICES),

        "profile_type": random.choice(PROFILES),

        "signup_date": fake.date_between(
            start_date="-5y",
            end_date="today"
        ),

        "account_status": random.choices(
            ACCOUNT_STATUS,
            weights=[92,8]
        )[0]

    })

df = pd.DataFrame(records)

output = RAW_DATA_DIR / "users.csv"

df.to_csv(output,index=False)

print("="*60)
print("USER DATA GENERATED")
print(df.head())
print("="*60)
print(f"Rows : {len(df)}")
print(f"Saved : {output}")