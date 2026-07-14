import json
import random
import time
import uuid
from pathlib import Path
from datetime import datetime

# =====================================================
# Output Folder
# =====================================================

OUTPUT_DIR = Path("streaming/events")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Master Data
# =====================================================

DEVICES = [
    "Mobile",
    "Smart TV",
    "Laptop",
    "Tablet",
    "Android TV",
    "Fire TV",
    "Apple TV"
]

PLANS = [
    "Basic",
    "Standard",
    "Premium"
]

COUNTRIES = [
    "India",
    "USA",
    "Canada",
    "UK",
    "Germany",
    "Japan"
]

NETWORKS = [
    "WiFi",
    "4G",
    "5G"
]

GENRES = [
    "Action",
    "Comedy",
    "Drama",
    "Romance",
    "Sci-Fi",
    "Documentary",
    "Thriller"
]

QUALITIES = [
    "480p",
    "720p",
    "1080p",
    "4K"
]

EVENTS = [
    "PLAY",
    "PAUSE",
    "STOP",
    "RESUME",
    "SEARCH",
    "LIKE",
    "DISLIKE",
    "SKIP"
]

# Keep one session per user
SESSIONS = {}

counter = 1

print("=" * 60)
print("OTT Live Event Generator Started")
print("=" * 60)

while True:

    user = f"USR-{random.randint(1,50000):06}"

    if user not in SESSIONS:
        SESSIONS[user] = str(uuid.uuid4())

    event = {

        "event_id": str(uuid.uuid4()),

        "timestamp": datetime.now().isoformat(),

        "user_id": user,

        "session_id": SESSIONS[user],

        "content_id": f"CNT-{random.randint(1,5000):05}",

        "event_type": random.choice(EVENTS),

        "device": random.choice(DEVICES),

        "subscription_plan": random.choice(PLANS),

        "country": random.choice(COUNTRIES),

        "network": random.choice(NETWORKS),

        "genre": random.choice(GENRES),

        "quality": random.choice(QUALITIES),

        "watch_seconds": random.randint(5,7200),

        "completion_pct": round(random.uniform(0,100),2),

        "buffer_time_ms": random.randint(0,5000),

        "rating": random.randint(1,5)

    }

    filename = OUTPUT_DIR / f"event_{counter:08}.json"

    with open(filename, "w") as f:
        json.dump(event, f)

    print(
        f"[{counter:06}] "
        f"{event['event_type']:<10}"
        f"{event['user_id']} "
        f"{event['device']}"
    )

    counter += 1

    time.sleep(1)