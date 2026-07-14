"""
=========================================================
OTT Analytics Platform
Central Logging Utility
=========================================================
"""

import logging
from pathlib import Path

from config import LOG_DIR

# ---------------------------------------------------------
# Create logs directory if it doesn't exist
# ---------------------------------------------------------

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "ott_platform.log"

# ---------------------------------------------------------
# Configure Logger
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ---------------------------------------------------------
# Logger Factory
# ---------------------------------------------------------

def get_logger(name: str):
    """
    Returns a configured logger.
    """

    return logging.getLogger(name)