from pathlib import Path
import pandas as pd


def load_raw_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def basic_data_audit(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
        "unique_stores": df["store"].nunique(),
        "unique_items": df["item"].nunique(),
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
    }