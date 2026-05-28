from itertools import product
import pandas as pd
from darts import TimeSeries


def create_hierarchical_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["store_item"] = df.apply(
        lambda x: f"store_{x['store']}_item_{x['item']}", axis=1
    )

    store_item_level = df.pivot(
        index="date", columns="store_item", values="sales"
    )

    store_level = (
        df.groupby(["date", "store"])["sales"]
        .sum()
        .reset_index()
        .pivot(index="date", columns="store", values="sales")
    )
    store_level.columns = [f"store_{c}" for c in store_level.columns]

    item_level = (
        df.groupby(["date", "item"])["sales"]
        .sum()
        .reset_index()
        .pivot(index="date", columns="item", values="sales")
    )
    item_level.columns = [f"item_{c}" for c in item_level.columns]

    total_level = (
        df.groupby("date")["sales"]
        .sum()
        .to_frame()
        .rename(columns={"sales": "Total"})
    )

    hierarchy_df = (
        store_item_level
        .join(store_level)
        .join(item_level)
        .join(total_level)
    )

    hierarchy_df.index = pd.to_datetime(hierarchy_df.index)
    hierarchy_df = hierarchy_df.sort_index()

    return hierarchy_df


def create_hierarchy_dict(df: pd.DataFrame) -> dict:
    stores = [f"store_{s}" for s in sorted(df["store"].unique())]
    items = [f"item_{i}" for i in sorted(df["item"].unique())]

    hierarchy = {}

    for store in stores:
        hierarchy[store] = ["Total"]

    for item in items:
        hierarchy[item] = ["Total"]

    for store, item in product(stores, items):
        hierarchy[f"{store}_{item}"] = [store, item]

    return hierarchy


def create_darts_series(hierarchy_df: pd.DataFrame, hierarchy: dict) -> TimeSeries:
    series = TimeSeries.from_dataframe(hierarchy_df)
    series = series.with_hierarchy(hierarchy)
    return series


def get_hierarchy_groups(df: pd.DataFrame) -> dict:
    stores = [f"store_{s}" for s in sorted(df["store"].unique())]
    items = [f"item_{i}" for i in sorted(df["item"].unique())]
    store_items = [
        f"store_{s}_item_{i}"
        for s, i in product(sorted(df["store"].unique()), sorted(df["item"].unique()))
    ]

    return {
        "total": ["Total"],
        "stores": stores,
        "items": items,
        "store_items": store_items,
    }