import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INTERVAL = 30


def run(name, command):

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True
    )

    if result.returncode != 0:
        print(f"{name} FAILED")
    else:
        print(f"{name} COMPLETED")


def main():

    print("=" * 80)
    print("OTT STREAM INTELLIGENCE PLATFORM SCHEDULER")
    print("=" * 80)

    while True:

        run(
            "Gold Pipeline",
            "python -m spark_jobs.gold.pipeline"
        )

        run(
            "Gold Loader",
            "python -m database.gold_loader"
        )

        print(f"\nSleeping {INTERVAL} seconds...\n")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()