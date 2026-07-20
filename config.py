import os
import sys
from pathlib import Path

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# Belt-and-suspenders fix: make sure PROJECT_ROOT is importable
# regardless of how a child script is launched (plain `python script.py`,
# `python -m package.script`, double-clicked, run from another cwd, etc).
# Without this, "from config import ..." breaks any time a generator is
# executed with a different working directory or sys.path[0].
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# DATA LAKE
# ==========================================================

DATA_LAKE = PROJECT_ROOT / "data_lake"

RAW_DATA_DIR = DATA_LAKE / "raw"
BRONZE_DIR = DATA_LAKE / "bronze"
SILVER_DIR = DATA_LAKE / "silver"
GOLD_DIR = DATA_LAKE / "gold"
CHECKPOINT_DIR = DATA_LAKE / "checkpoints"

# ==========================================================
# STREAMING
# ==========================================================

STREAMING_DIR = PROJECT_ROOT / "streaming"
EVENTS_DIR = STREAMING_DIR / "events"

# ==========================================================
# ML
# ==========================================================

ML_MODELS_DIR = PROJECT_ROOT / "ml_models"

# ==========================================================
# AUTO CREATE
# ==========================================================

REQUIRED_DIRS = [
    RAW_DATA_DIR,
    BRONZE_DIR,
    SILVER_DIR,
    GOLD_DIR,
    CHECKPOINT_DIR,
    EVENTS_DIR,
    ML_MODELS_DIR,
]

for folder in REQUIRED_DIRS:
    folder.mkdir(parents=True, exist_ok=True)

# ==========================================================
# MYSQL
# ==========================================================
# Credentials are read from environment variables first so real
# passwords never sit in version control. The literals below are
# local-dev fallbacks only — override them via a .env file or your
# shell environment for anything beyond your own machine.

DB_HOST = os.environ.get("OTT_DB_HOST", "localhost")
DB_PORT = int(os.environ.get("OTT_DB_PORT", "3306"))
DB_USER = os.environ.get("OTT_DB_USER", "root")
DB_PASSWORD = os.environ.get("OTT_DB_PASSWORD", "1234")
DB_NAME = os.environ.get("OTT_DB_NAME", "ott_analytics")

# ==========================================================
# SYNTHETIC DATASET SCALE
# ==========================================================

# Historical platform size
TOTAL_USERS = 50000

# Historical watch history
WATCH_EVENTS = 250000

# Historical sessions
SESSION_EVENTS = 250000

# Content catalog
TOTAL_CONTENT = 5000

# Subscription records
TOTAL_SUBSCRIPTIONS = TOTAL_USERS

# ==========================================================
# DERIVED GENERATOR COUNTS
# ==========================================================

# Ratings generated from watch history (~40% of watch events)
TOTAL_RATINGS = int(WATCH_EVENTS * 0.4)

# Search events generated for the platform
SEARCH_EVENTS = int(TOTAL_USERS * 5)