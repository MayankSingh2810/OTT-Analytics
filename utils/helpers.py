"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
Utility Helper Functions
============================================================
"""

import uuid


# ==========================================================
# GENERIC UNIQUE ID GENERATOR
# ==========================================================

def generate_unique_id(prefix: str) -> str:
    """
    Generates a globally unique ID.

    Example:
        USR-550E8400E29B41D4A716446655440000
        CNT-550E8400E29B41D4A716446655440000
    """

    return f"{prefix}-{uuid.uuid4().hex.upper()}"


# ==========================================================
# ENTITY ID GENERATORS
# ==========================================================

def generate_user_id():
    return generate_unique_id("USR")


def generate_content_id():
    return generate_unique_id("CNT")


def generate_subscription_id():
    return generate_unique_id("SUB")


def generate_watch_id():
    return generate_unique_id("WAT")


def generate_rating_id():
    return generate_unique_id("RAT")


def generate_session_id():
    return generate_unique_id("SES")


def generate_search_id():
    return generate_unique_id("SRCH")