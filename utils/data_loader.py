import pandas as pd
import os
from functools import lru_cache

DATA_PATH = "data"

def get_all_sectors():
    files = os.listdir(DATA_PATH)
    return [f.replace(".xlsx", "") for f in files if f.endswith(".xlsx")]

@lru_cache(maxsize=32)
def load_sector_data(sector):
    path = f"{DATA_PATH}/{sector}.xlsx"
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def get_unique_values(df, col):
    if col not in df.columns:
        return []
    return sorted(df[col].dropna().unique())