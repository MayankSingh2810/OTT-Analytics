from config import RAW_DATA_DIR

from database.csv_loader import CSVLoader

loader = CSVLoader(
    RAW_DATA_DIR / "users.csv"
)

df = loader.load()

loader.validate(df)

print(df.head())