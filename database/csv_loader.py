"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
CSV Loader Utility
============================================================
"""

from pathlib import Path

import pandas as pd


class CSVLoader:
    """
    Generic CSV Loader with validation.
    """

    def __init__(self, csv_path: Path):

        self.csv_path = Path(csv_path)

    # ==========================================================
    # LOAD CSV
    # ==========================================================

    def load(self):

        if not self.csv_path.exists():

            raise FileNotFoundError(
                f"{self.csv_path} not found."
            )

        print("=" * 70)
        print(f"Loading : {self.csv_path.name}")

        df = pd.read_csv(self.csv_path)

        print(f"Rows : {len(df):,}")
        print(f"Columns : {len(df.columns)}")

        return df

    # ==========================================================
    # VALIDATE
    # ==========================================================

    @staticmethod
    def validate(df):

        print("-" * 70)

        print("Checking Null Values...")

        print(df.isnull().sum())

        print("-" * 70)

        print("Duplicate Rows :", df.duplicated().sum())

        print("-" * 70)

        print("Validation Complete")

        print("=" * 70)