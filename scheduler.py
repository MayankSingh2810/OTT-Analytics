import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

INTERVAL = 30  # seconds


def run_step(name, command):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True
    )

    if result.returncode == 0:
        print(f"✓ {name} completed successfully")
    else:
        print(f"✗ {name} failed")


def main():
    print("=" * 60)
    print("OTT Stream Intelligence Platform Scheduler")
    print("=" * 60)

    while True:

        print("\nStarting new pipeline cycle...\n")

        # ==========================================================
        # STEP 1 : Generate Live Events
        # ==========================================================

        run_step(
            "Event Generator",
            "python event_generator/generate_events.py"
        )

        print(f"\nWaiting {INTERVAL} seconds...")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()