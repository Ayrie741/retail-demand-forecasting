import numpy as np
import pandas as pd


def _to_pandas_series(ts):
    """
    Convert a selected Darts TimeSeries component to a pandas Series.

    This avoids version issues with older Darts methods such as pd_series().
    """
    return ts.to_dataframe().iloc[:, 0]


def _align_component_series(actual_component, predicted_component) -> tuple[np.ndarray, np.ndarray]:
    """
    Align one actual component and one predicted component by timestamp.
    """

    actual_series = _to_pandas_series(actual_component)
    pred_series = _to_pandas_series(predicted_component)

    aligned = pd.concat(
        [actual_series.rename("actual"), pred_series.rename("predicted")],
        axis=1,
        join="inner"
    ).dropna()

    y_true = aligned["actual"].to_numpy(dtype=float)
    y_pred = aligned["predicted"].to_numpy(dtype=float)

    return y_true, y_pred


def _mape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-8) -> float:
    denominator = np.maximum(np.abs(y_true), eps)
    return np.mean(np.abs((y_true - y_pred) / denominator)) * 100


def _smape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-8) -> float:
    denominator = np.maximum(np.abs(y_true) + np.abs(y_pred), eps)
    return np.mean(2 * np.abs(y_pred - y_true) / denominator) * 100


def _mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(np.abs(y_true - y_pred))


def _rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def evaluate_group(actual, predicted, components: list, group_name: str) -> dict:
    """
    Evaluate forecast performance for one hierarchy level.

    The metric is calculated for each component first, then averaged across
    all components within the same hierarchy level.
    """

    mape_values = []
    smape_values = []
    mae_values = []
    rmse_values = []

    for component in components:
        y_true, y_pred = _align_component_series(
            actual[component],
            predicted[component]
        )

        mape_values.append(_mape(y_true, y_pred))
        smape_values.append(_smape(y_true, y_pred))
        mae_values.append(_mae(y_true, y_pred))
        rmse_values.append(_rmse(y_true, y_pred))

    return {
        "level": group_name,
        "MAPE": round(float(np.mean(mape_values)), 4),
        "sMAPE": round(float(np.mean(smape_values)), 4),
        "MAE": round(float(np.mean(mae_values)), 4),
        "RMSE": round(float(np.mean(rmse_values)), 4),
    }


def evaluate_all_levels(actual, predicted, hierarchy_groups: dict, model_name: str) -> pd.DataFrame:
    """
    Evaluate one forecast across all hierarchy levels.
    """

    rows = [
        evaluate_group(actual, predicted, hierarchy_groups["total"], "Total"),
        evaluate_group(actual, predicted, hierarchy_groups["stores"], "Store"),
        evaluate_group(actual, predicted, hierarchy_groups["items"], "Item"),
        evaluate_group(actual, predicted, hierarchy_groups["store_items"], "Store-Item"),
    ]

    result = pd.DataFrame(rows)
    result.insert(0, "model", model_name)

    return result


def calculate_coherence_gap(predicted, stores, items, store_items) -> pd.DataFrame:
    """
    Calculate forecast coherence gaps.
    """

    total = _to_pandas_series(predicted["Total"])
    sum_store = sum([_to_pandas_series(predicted[s]) for s in stores])
    sum_item = sum([_to_pandas_series(predicted[i]) for i in items])
    sum_store_item = sum([_to_pandas_series(predicted[si]) for si in store_items])

    gap_df = pd.DataFrame({
        "Total": total,
        "Sum_Store": sum_store,
        "Sum_Item": sum_item,
        "Sum_Store_Item": sum_store_item,
    })

    gap_df["Store_Gap"] = gap_df["Sum_Store"] - gap_df["Total"]
    gap_df["Item_Gap"] = gap_df["Sum_Item"] - gap_df["Total"]
    gap_df["Store_Item_Gap"] = gap_df["Sum_Store_Item"] - gap_df["Total"]

    gap_df["Abs_Store_Gap"] = gap_df["Store_Gap"].abs()
    gap_df["Abs_Item_Gap"] = gap_df["Item_Gap"].abs()
    gap_df["Abs_Store_Item_Gap"] = gap_df["Store_Item_Gap"].abs()

    return gap_df