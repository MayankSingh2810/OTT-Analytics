import json
import random
import time
import uuid
from pathlib import Path
from datetime import datetime
from collections import deque

# =====================================================
# CONFIGURATION
# =====================================================

OUTPUT_DIR = Path("streaming/events")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EVENTS_PER_SECOND = 1
MAX_EVENT_FILES = 500

# =====================================================
# MASTER DATA
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

# =====================================================
# SESSION CACHE
# =====================================================

SESSIONS = {}

recent_files = deque(maxlen=MAX_EVENT_FILES)

counter = 1

print("=" * 60)
print("OTT Live Event Generator Started")
print("=" * 60)

while True:

    for _ in range(EVENTS_PER_SECOND):

        user = f"USR-{random.randint(1,50000):06}"

        if user not in SESSIONS:
            SESSIONS[user] = str(uuid.uuid4())

        event_type = random.choices(
            EVENTS,
            weights=[40,8,6,8,15,10,5,8],
            k=1
        )[0]

        watch_seconds = random.randint(30,7200)

        completion = min(
            100,
            round((watch_seconds/7200)*100 + random.uniform(-5,5),2)
        )

        event = {

            "event_id": str(uuid.uuid4()),

            "timestamp": datetime.now().isoformat(),

            "user_id": user,

            "session_id": SESSIONS[user],

            "content_id": f"CNT-{random.randint(1,5000):05}",

            "event_type": event_type,

            "device": random.choice(DEVICES),

            "subscription_plan": random.choice(PLANS),

            "country": random.choice(COUNTRIES),

            "network": random.choice(NETWORKS),

            "genre": random.choice(GENRES),

            "quality": random.choice(QUALITIES),

            "watch_seconds": watch_seconds,

            "completion_pct": completion,

            "buffer_time_ms": random.randint(0,3000),

            "rating": random.randint(1,5)

        }

        filename = OUTPUT_DIR / f"event_{counter:08}.json"

        with open(filename, "w") as f:
            json.dump(event, f)

        recent_files.append(filename)

        if len(recent_files) == MAX_EVENT_FILES:
            oldest = recent_files[0]
            if oldest.exists():
                oldest.unlink()

        print(
            f"[{counter:08}] "
            f"{event_type:<8} "
            f"{user} "
            f"{event['device']}"
        )

        counter += 1

    time.sleep(1)