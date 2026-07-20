"""
==========================================================
Enterprise Big Data Pipeline
Historical + Live + Live Users
==========================================================
"""

from spark_jobs.gold.load_all_users import load_all_users
from spark_jobs.gold.build_gold_layer import build_gold_layer


def run_pipeline():

    print("\n")
    print("=" * 80)
    print("OTT ENTERPRISE DATA PIPELINE")
    print("=" * 80)

    # ---------------------------------------------------
    # Step 1
    # Merge Historical Users + Live Users
    # ---------------------------------------------------

    print("\nLoading Latest Users...\n")
    load_all_users()

    # ---------------------------------------------------
    # Step 2
    # Build Gold Layer
    # ---------------------------------------------------

    print("\nBuilding Gold Layer...\n")
    build_gold_layer()

    print("\n")
    print("=" * 80)
    print("PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()