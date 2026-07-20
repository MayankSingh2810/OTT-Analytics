"""
==========================================================
LIVE USER REGISTRATION GENERATOR
==========================================================
Creates NEW OTT users continuously
Output:
streaming/new_users/
==========================================================
"""

import json
import random
import time
import uuid
from pathlib import Path
from datetime import datetime

from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("streaming/new_users")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COUNTRIES = [
    ("India", "Hindi"),
    ("USA", "English"),
    ("Canada", "English"),
    ("UK", "English"),
    ("Australia", "English")
]

GENRES = [
    "Action",
    "Comedy",
    "Drama",
    "Crime",
    "Thriller",
    "Sci-Fi",
    "Romance",
    "Fantasy",
    "Documentary",
    "Horror"
]

DEVICES = [
    "Mobile",
    "Laptop",
    "Tablet",
    "Smart TV",
    "Fire TV",
    "Apple TV",
    "Android TV"
]

PLANS = [
    "Basic",
    "Standard",
    "Premium"
]


def create_user():

    country, language = random.choice(COUNTRIES)

    return {

        "user_id": "USR-" + uuid.uuid4().hex.upper(),

        "first_name": fake.first_name(),

        "last_name": fake.last_name(),

        "email": fake.email(),

        "gender": random.choice(["Male", "Female"]),

        "age": random.randint(18, 75),

        "country": country,

        "city": fake.city(),

        "preferred_language": language,

        "preferred_genre": random.choice(GENRES),

        "device_type": random.choice(DEVICES),

        "profile_type": random.choice(
            ["Single", "Family", "Kids"]
        ),

        "signup_date": datetime.now().strftime("%Y-%m-%d"),

        "account_status": "Active",

        "subscription_plan": random.choice(PLANS)

    }


print("=" * 70)
print("LIVE USER GENERATOR STARTED")
print("=" * 70)

batch = 1

while True:

    records = []

    new_users = random.randint(5, 15)

    for _ in range(new_users):
        records.append(create_user())

    filename = OUTPUT_DIR / f"users_batch_{batch}.json"

    with open(filename, "w") as f:
        for row in records:
            f.write(json.dumps(row))
            f.write("\n")

    print(
        f"Batch {batch} | {new_users} new users generated"
    )

    batch += 1

    time.sleep(30)