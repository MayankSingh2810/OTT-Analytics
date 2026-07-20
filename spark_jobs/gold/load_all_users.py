"""
==========================================================
Load Historical Users + Live Users
Enterprise Gold Utility
==========================================================
"""

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

from config import SILVER_DIR


def load_all_users(spark: SparkSession) -> DataFrame:
    """
    Returns one unified users dataframe.

    Historical Users
        +
    Live Streamed Users

    Duplicate user_ids are removed.
    """

    # ===============================================
    # Historical Users
    # ===============================================

    historical_users = (
        spark.read.parquet(
            str(SILVER_DIR / "users")
        )
        .withColumn("source", lit("historical"))
    )

    # ===============================================
    # Live Users
    # ===============================================

    try:

        live_users = (
            spark.read.parquet(
                str(SILVER_DIR / "live_users")
            )
            .withColumn("source", lit("live"))
        )

        users = (
            historical_users
            .unionByName(
                live_users,
                allowMissingColumns=True
            )
        )

    except Exception:

        # live_users folder doesn't exist yet
        users = historical_users

    # ===============================================
    # Remove duplicates
    # ===============================================

    users = users.dropDuplicates(["user_id"])

    return users