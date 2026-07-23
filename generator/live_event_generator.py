import json
import random
import time
import uuid
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import deque

from config import RAW_DATA_DIR  # <-- FIX: use the same base path config.py uses

# =====================================================
# CONFIGURATION
# =====================================================

OUTPUT_DIR = Path("streaming/events")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load REAL Content IDs
# =====================================================

content_df = pd.read_csv(RAW_DATA_DIR / "content.csv")

CONTENT_IDS = content_df["content_id"].tolist()

print(f"Loaded {len(CONTENT_IDS)} content IDs")

# =====================================================
# Load REAL User IDs
# =====================================================

# FIX: the generator was inventing sequential IDs like "USR-000172"
# that never existed in users.csv (real IDs are UUID-based, e.g.
# "USR-0010F2AA94884AFB9C78C8541E9B0DB4"). That mismatch is why every
# live event failed to join to country/subscription/demographics
# downstream (830 NULL rows in country_stats, churn_features, etc.).
# Now we load and reuse the actual user_id pool from users.csv.

users_df = pd.read_csv(RAW_DATA_DIR / "users.csv")

USER_IDS = users_df["user_id"].tolist()

print(f"Loaded {len(USER_IDS)} users")

# Bumped back to 150 per checklist. Previously reduced to 75 "until
# pipeline throughput is verified" -- if that verification hasn't
# actually happened yet, watch for backpressure/lag downstream.
EVENTS_PER_SECOND = 150
MAX_EVENT_FILES = 50000

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

# Event distribution skewed toward PLAY, matching real
# streaming behavior (users mostly just hit play).
EVENT_WEIGHTS = [
    55,   # PLAY
    8,    # PAUSE
    6,    # STOP
    10,   # RESUME
    8,    # SEARCH
    8,    # LIKE
    2,    # DISLIKE
    3     # SKIP
]

# =====================================================
# SESSION CACHE
# =====================================================

SESSIONS = {}

recent_files = deque(maxlen=MAX_EVENT_FILES)

counter = 1

print("=" * 60)
print("OTT Live Event Generator Started")
print(f"Events/sec: {EVENTS_PER_SECOND}  |  Users: {len(USER_IDS)}")
print("=" * 60)


def generate_watch_seconds():
    """
    Bucketed watch-time distribution so short, medium, long,
    and binge sessions occur in realistic proportions instead of a
    flat uniform 30-7200s range.
    """
    return random.choices(
        population=[
            random.randint(30, 300),      # short clips / previews
            random.randint(300, 1200),    # short-to-medium episodes
            random.randint(1200, 3600),   # full episodes / short movies
            random.randint(3600, 7200)    # movies / binge sessions
        ],
        weights=[30, 35, 25, 10],
        k=1
    )[0]


def generate_completion(watch_seconds):
    """
    Completion % scaled against a more realistic "typical
    content length" denominator (5400s ~ 90 min) with noise, clamped
    to [0, 100].
    """
    return round(
        min(
            100,
            max(
                0,
                (watch_seconds / 5400) * 100 + random.uniform(-8, 8)
            )
        ),
        2
    )


def generate_event(counter):
    """Build a single event dict. Pulled out of the loop so it's testable
    and reusable without touching global state beyond SESSIONS."""
    user = random.choice(USER_IDS)

    if user not in SESSIONS:
        SESSIONS[user] = str(uuid.uuid4())

    event_type = random.choices(EVENTS, weights=EVENT_WEIGHTS, k=1)[0]

    watch_seconds = generate_watch_seconds()
    completion = generate_completion(watch_seconds)

    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "user_id": user,
        "session_id": SESSIONS[user],
        "content_id": random.choice(CONTENT_IDS),
        "event_type": event_type,
        "device": random.choice(DEVICES),
        "subscription_plan": random.choice(PLANS),
        "country": random.choice(COUNTRIES),
        "network": random.choice(NETWORKS),
        "genre": random.choice(GENRES),
        "quality": random.choice(QUALITIES),
        "watch_seconds": watch_seconds,
        "completion_pct": completion,
        "buffer_time_ms": random.randint(0, 3000),
        "rating": random.randint(1, 5),
    }


def main():
    global counter

    while True:
        for _ in range(EVENTS_PER_SECOND):
            event = generate_event(counter)

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
                f"{event['event_type']:<8} "
                f"{event['user_id']} "
                f"{event['device']}"
            )

            counter += 1

        time.sleep(1)


if __name__ == "__main__":
    main()