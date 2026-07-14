import pandas as pd

from config import TABLES


def load_table(name):

    path = TABLES.get(name)

    if path is None:

        return pd.DataFrame()

    if not path.exists():

        return pd.DataFrame()

    try:

        return pd.read_parquet(path)

    except Exception as e:

        print(e)

        return pd.DataFrame()