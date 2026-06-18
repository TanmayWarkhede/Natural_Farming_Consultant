"""
Market intelligence utilities – reads crop_prices.csv and computes stats.
"""
import os
import pandas as pd
from typing import Optional

from config.settings import DATA_FOLDER


CSV_PATH = os.path.join(DATA_FOLDER, "crop_prices.csv")


def load_crop_prices() -> Optional[pd.DataFrame]:
    """Load crop_prices.csv; return None if file is missing or malformed."""
    try:
        if not os.path.exists(CSV_PATH):
            return None
        df = pd.read_csv(CSV_PATH)
        required_cols = {"crop", "price_per_quintal", "category"}
        if not required_cols.issubset(set(df.columns.str.lower())):
            df.columns = df.columns.str.lower()
        df["price_per_quintal"] = pd.to_numeric(df["price_per_quintal"], errors="coerce")
        df = df.dropna(subset=["price_per_quintal"])
        return df
    except Exception:
        return None


def compute_market_summary(df: pd.DataFrame) -> dict:
    """Return aggregated stats from the price dataframe."""
    if df is None or df.empty:
        return {}

    highest_row = df.loc[df["price_per_quintal"].idxmax()]
    lowest_row = df.loc[df["price_per_quintal"].idxmin()]
    avg_price = df["price_per_quintal"].mean()
    top_crops = (
        df.nlargest(3, "price_per_quintal")[["crop", "price_per_quintal"]]
        .to_dict(orient="records")
    )

    return {
        "total_crops": len(df),
        "highest_crop": highest_row["crop"],
        "highest_price": round(float(highest_row["price_per_quintal"]), 2),
        "lowest_crop": lowest_row["crop"],
        "lowest_price": round(float(lowest_row["price_per_quintal"]), 2),
        "avg_price": round(float(avg_price), 2),
        "top_crops": top_crops,
    }


def get_category_stats(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Return mean price per category."""
    if df is None or df.empty or "category" not in df.columns:
        return None
    return (
        df.groupby("category")["price_per_quintal"]
        .mean()
        .reset_index()
        .rename(columns={"price_per_quintal": "avg_price"})
        .sort_values("avg_price", ascending=False)
        .round(2)
    )


def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """Filter dataframe by crop category."""
    if df is None or df.empty:
        return pd.DataFrame()
    if "category" not in df.columns:
        return df
    if category == "All":
        return df
    return df[df["category"] == category]
