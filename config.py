from pathlib import Path

# ==========================================================
# PROJECT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

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

for folder in [
    RAW_DATA_DIR,
    BRONZE_DIR,
    SILVER_DIR,
    GOLD_DIR,
    CHECKPOINT_DIR,
    EVENTS_DIR,
    ML_MODELS_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)