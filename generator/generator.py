import subprocess
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def start_background(name, command):
    print(f"\n{'='*60}")
    print(f"Starting {name}")
    print(f"{'='*60}")

    return subprocess.Popen(
        command,
        cwd=PROJECT_ROOT,
        shell=True
    )


def run_step(name, command):
    print(f"\nRunning {name}...")

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True
    )

    if result.returncode == 0:
        print(f"✓ {name} Completed")
    else:
        print(f"✗ {name} Failed")


def main():

    print("=" * 70)
    print("OTT STREAM INTELLIGENCE PLATFORM")
    print("=" * 70)

    # Live Event Generator
    event_process = start_background(
        "Live Event Generator",
        "python generator/live_event_generator.py"
    )

    # Bronze Streaming
    bronze_process = start_background(
        "Bronze Streaming",
        "python spark_jobs/streaming_bronze.py"
    )

    print("\nWaiting for live data...\n")
    time.sleep(15)

    while True:

        print("\n================ NEW PIPELINE CYCLE ================\n")

        run_step(
            "Silver Pipeline",
            "python spark_jobs/silver/pipeline.py"
        )

        run_step(
            "Gold Pipeline",
            "python spark_jobs/gold/pipeline.py"
        )

        run_step(
            "Feature Store",
            "python spark_jobs/ml/feature_store.py"
        )

        run_step(
            "Random Forest",
            "python spark_jobs/ml/random_forest.py"
        )

        run_step(
            "Gradient Boosted Trees",
            "python spark_jobs/ml/gradient_boosted.py"
        )

        run_step(
            "ALS Recommendation",
            "python spark_jobs/ml/als_recommendation.py"
        )

        run_step(
            "Forecast",
            "python spark_jobs/ml/forecast.py"
        )

        run_step(
            "Model Evaluation",
            "python spark_jobs/ml/evaluate.py"
        )

        print("\nPipeline cycle completed.")
        print("Sleeping for 30 seconds...\n")

        time.sleep(30)


if __name__ == "__main__":
    main()