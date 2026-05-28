import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


PASTEL_PINK = "#F4B6B6"
PASTEL_GREEN = "#B7DDB4"
PASTEL_BLUE = "#B8D8E8"
PASTEL_YELLOW = "#F3D9A4"
PASTEL_PURPLE = "#D6C4E9"
TEXT_DARK = "#3A3A3A"
GRID_LIGHT = "#EAEAEA"

def _to_pandas_series(ts):
    """
    Convert a selected Darts TimeSeries component to a pandas Series.
    """
    return ts.to_dataframe().iloc[:, 0]

def set_project_style():
    """
    Set a consistent low-saturation visual style for the notebook.
    """

    plt.rcParams.update({
        "figure.figsize": (12, 5),
        "figure.dpi": 120,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "axes.edgecolor": "#DDDDDD",
        "axes.labelcolor": TEXT_DARK,
        "xtick.color": TEXT_DARK,
        "ytick.color": TEXT_DARK,
        "text.color": TEXT_DARK,
        "axes.titleweight": "bold",
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "legend.frameon": True,
        "legend.facecolor": "white",
        "legend.edgecolor": "#DDDDDD",
        "grid.color": GRID_LIGHT,
        "grid.linestyle": "-",
        "grid.linewidth": 0.8,
    })


def _annotate_point(ax, x, y, label, color=PASTEL_PINK, xytext=(10, 12)):
    ax.annotate(
        label,
        xy=(x, y),
        xytext=xytext,
        textcoords="offset points",
        fontsize=9,
        bbox=dict(
            boxstyle="round,pad=0.3",
            fc=color,
            ec=color,
            alpha=0.45
        ),
        arrowprops=dict(
            arrowstyle="->",
            color=color,
            lw=1.2
        )
    )


def plot_total_sales(df: pd.DataFrame, save_path=None):
    """
    Plot total daily sales and highlight key points:
    - start point
    - end point
    - maximum daily sales
    """

    set_project_style()

    daily_total = df.groupby("date")["sales"].sum()
    daily_total.index = pd.to_datetime(daily_total.index)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        daily_total.index,
        daily_total.values,
        color=PASTEL_GREEN,
        linewidth=2.2,
        label="Daily total sales"
    )

    ax.set_title("Daily Total Sales Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sales")
    ax.grid(True, alpha=0.8)

    start_date = daily_total.index.min()
    end_date = daily_total.index.max()
    max_date = daily_total.idxmax()

    _annotate_point(
        ax,
        start_date,
        daily_total.loc[start_date],
        f"Start\n{daily_total.loc[start_date]:,.0f}",
        color=PASTEL_PINK
    )

    _annotate_point(
        ax,
        end_date,
        daily_total.loc[end_date],
        f"End\n{daily_total.loc[end_date]:,.0f}",
        color=PASTEL_PINK,
        xytext=(-55, 12)
    )

    _annotate_point(
        ax,
        max_date,
        daily_total.loc[max_date],
        f"Peak\n{daily_total.loc[max_date]:,.0f}",
        color=PASTEL_GREEN,
        xytext=(-35, 18)
    )

    ax.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_forecast_coherence(predicted, stores, items, store_items, title, save_path=None):
    """
    Plot whether forecasts are coherent across hierarchy levels.

    The legend is placed outside the plot area to avoid covering the final-day
    data label. The final-day annotation is positioned to the left-bottom side
    of the last point for better readability.
    """

    set_project_style()

    total_series = _to_pandas_series(predicted["Total"])
    store_sum = sum([_to_pandas_series(predicted[s]) for s in stores])
    item_sum = sum([_to_pandas_series(predicted[i]) for i in items])
    store_item_sum = sum([_to_pandas_series(predicted[si]) for si in store_items])

    fig, ax = plt.subplots(figsize=(14, 5.5))

    ax.plot(
        total_series.index,
        total_series.values,
        label="Predicted Total",
        color=PASTEL_PINK,
        linewidth=3.0,
        alpha=0.9
    )

    ax.plot(
        store_sum.index,
        store_sum.values,
        label="Sum of Store Forecasts",
        color=PASTEL_GREEN,
        linewidth=2.3,
        alpha=0.9
    )

    ax.plot(
        item_sum.index,
        item_sum.values,
        label="Sum of Item Forecasts",
        color=PASTEL_BLUE,
        linewidth=2.3,
        alpha=0.9
    )

    ax.plot(
        store_item_sum.index,
        store_item_sum.values,
        label="Sum of Store-Item Forecasts",
        color=PASTEL_YELLOW,
        linewidth=2.3,
        alpha=0.9
    )

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Forecasted Sales")
    ax.grid(True, alpha=0.8)

    # Add vertical padding so annotation is not too close to the plot boundary
    all_values = pd.concat(
        [total_series, store_sum, item_sum, store_item_sum],
        axis=1
    )

    y_min = all_values.min().min()
    y_max = all_values.max().max()
    y_padding = (y_max - y_min) * 0.12

    ax.set_ylim(y_min - y_padding, y_max + y_padding)

    # Final-day annotation
    last_date = total_series.index[-1]

    label_text = (
        f"Final day\n"
        f"Total: {total_series.loc[last_date]:,.0f}\n"
        f"Store sum: {store_sum.loc[last_date]:,.0f}\n"
        f"Item sum: {item_sum.loc[last_date]:,.0f}\n"
        f"Store-item sum: {store_item_sum.loc[last_date]:,.0f}"
    )

    ax.scatter(
        last_date,
        total_series.loc[last_date],
        color=PASTEL_PINK,
        s=45,
        zorder=5
    )

    ax.annotate(
        label_text,
        xy=(last_date, total_series.loc[last_date]),
        xytext=(-170, -75),
        textcoords="offset points",
        fontsize=9,
        ha="left",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.35",
            fc=PASTEL_PINK,
            ec=PASTEL_PINK,
            alpha=0.35
        ),
        arrowprops=dict(
            arrowstyle="->",
            color=PASTEL_PINK,
            lw=1.2
        )
    )

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0,
        frameon=True
    )

    plt.tight_layout(rect=[0, 0, 0.82, 1])

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_metric_comparison(result_df: pd.DataFrame, metric="MAPE", save_path=None):
    """
    Compare model performance across hierarchy levels.
    """

    set_project_style()

    pivot_df = result_df.pivot(index="level", columns="model", values=metric)

    ax = pivot_df.plot(
        kind="bar",
        figsize=(12, 5),
        color=[PASTEL_PINK, PASTEL_GREEN, PASTEL_BLUE, PASTEL_YELLOW, PASTEL_PURPLE]
    )

    ax.set_title(f"{metric} Comparison Across Hierarchy Levels")
    ax.set_ylabel(metric)
    ax.set_xlabel("Hierarchy Level")
    ax.grid(axis="y", alpha=0.8)
    plt.xticks(rotation=0)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", fontsize=8, padding=3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_coherence_gap_summary(gap_df: pd.DataFrame, save_path=None):
    """
    Summarize average absolute coherence gaps before or after reconciliation.
    """

    set_project_style()

    summary = pd.Series({
        "Store gap": gap_df["Abs_Store_Gap"].mean(),
        "Item gap": gap_df["Abs_Item_Gap"].mean(),
        "Store-item gap": gap_df["Abs_Store_Item_Gap"].mean(),
    }).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(
        summary.index,
        summary.values,
        color=[PASTEL_PINK, PASTEL_GREEN, PASTEL_BLUE]
    )

    ax.set_title("Average Absolute Forecast Coherence Gap")
    ax.set_ylabel("Average absolute gap")
    ax.grid(axis="y", alpha=0.8)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()