"""
==========================================================
Enterprise Big Data Pipeline
==========================================================
"""

from spark_jobs.gold.build_gold_layer import build_gold_layer


def run_pipeline():

    print("\n")
    print("=" * 80)
    print("OTT ENTERPRISE DATA PIPELINE")
    print("=" * 80)

    print("\nBuilding Gold Layer...\n")

    build_gold_layer()

    print("\n")
    print("=" * 80)
    print("PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()