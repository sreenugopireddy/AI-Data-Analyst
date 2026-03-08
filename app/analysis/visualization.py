"""
analysis/visualization.py — Chart generation layer.

Each function returns a Matplotlib Figure object so Streamlit can render
it with st.pyplot() without any global state side-effects.
"""

import warnings
import matplotlib
matplotlib.use("Agg")   # Non-interactive backend — required for Streamlit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
from analysis.data_loader import get_column_types
from analysis.statistics import _find_column, compute_revenue_trend
from config import CHART_PALETTE, CHART_STYLE, CHART_DPI, FIGURE_SIZE_WIDE, FIGURE_SIZE_SQUARE

# Suppress harmless matplotlib/seaborn deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

plt.style.use(CHART_STYLE)


# ── Public chart functions ────────────────────────────────────────────────────

def plot_revenue_trend(df: pd.DataFrame) -> plt.Figure | None:
    """
    Line chart: aggregated revenue / primary numeric metric over time.
    Returns None if no datetime column exists.
    """
    trend = compute_revenue_trend(df)
    if trend is None or trend.empty:
        return None

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE, dpi=CHART_DPI)

    ax.plot(
        trend["period"],
        trend["revenue"],
        marker="o",
        linewidth=2.5,
        color=CHART_PALETTE[0],
        markersize=7,
        markerfacecolor="white",
        markeredgewidth=2,
    )
    ax.fill_between(
        trend["period"],
        trend["revenue"],
        alpha=0.12,
        color=CHART_PALETTE[0],
    )

    ax.set_title("Revenue Trend Over Time", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Period", fontsize=11)
    ax.set_ylabel("Revenue ($)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.xticks(rotation=35, ha="right")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def plot_product_performance(df: pd.DataFrame) -> plt.Figure | None:
    """
    Horizontal bar chart: total revenue per product / top category.
    Returns None if no suitable columns are found.
    """
    product_col = _find_column(df, ["product", "item", "sku", "name"])
    revenue_col = _find_column(df, ["revenue", "sales", "amount", "total"])

    if product_col is None or revenue_col is None:
        # Fallback: top numeric column grouped by first categorical
        col_types = get_column_types(df)
        if not col_types["categorical"] or not col_types["numeric"]:
            return None
        product_col = col_types["categorical"][0]
        revenue_col = col_types["numeric"][0]

    grouped = (
        df.groupby(product_col)[revenue_col]
        .sum()
        .sort_values(ascending=True)
        .tail(10)   # Show top-10
    )

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE, dpi=CHART_DPI)

    bars = ax.barh(
        grouped.index,
        grouped.values,
        color=CHART_PALETTE[:len(grouped)],
        height=0.6,
        edgecolor="none",
    )

    # Add value labels to each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width * 1.01, bar.get_y() + bar.get_height() / 2,
            f"${width:,.0f}",
            va="center", ha="left", fontsize=9, color="#444",
        )

    ax.set_title("Product Performance (Total Revenue)", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Total Revenue ($)", fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    _style_axes(ax)
    fig.tight_layout()
    return fig


def plot_category_comparison(df: pd.DataFrame) -> plt.Figure | None:
    """
    Grouped bar chart: revenue broken down by category.
    Falls back to a donut chart for a single categorical column.
    """
    cat_col = _find_column(df, ["category", "type", "segment", "group", "dept"])
    revenue_col = _find_column(df, ["revenue", "sales", "amount", "total"])

    col_types = get_column_types(df)
    if cat_col is None and col_types["categorical"]:
        cat_col = col_types["categorical"][0]
    if revenue_col is None and col_types["numeric"]:
        revenue_col = col_types["numeric"][0]
    if cat_col is None or revenue_col is None:
        return None

    grouped = df.groupby(cat_col)[revenue_col].sum().sort_values(ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=CHART_DPI)

    # Left: bar chart
    ax_bar = axes[0]
    ax_bar.bar(
        grouped.index,
        grouped.values,
        color=CHART_PALETTE[:len(grouped)],
        width=0.55,
        edgecolor="none",
    )
    ax_bar.set_title(f"Revenue by {cat_col.title()}", fontsize=13, fontweight="bold")
    ax_bar.set_ylabel("Total Revenue ($)", fontsize=10)
    ax_bar.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.setp(ax_bar.get_xticklabels(), rotation=25, ha="right", fontsize=9)
    _style_axes(ax_bar)

    # Right: donut chart
    ax_pie = axes[1]
    wedge_props = {"width": 0.55, "edgecolor": "white", "linewidth": 2}
    ax_pie.pie(
        grouped.values,
        labels=grouped.index,
        colors=CHART_PALETTE[:len(grouped)],
        autopct="%1.1f%%",
        pctdistance=0.75,
        wedgeprops=wedge_props,
        textprops={"fontsize": 9},
    )
    ax_pie.set_title("Revenue Share (%)", fontsize=13, fontweight="bold")

    fig.tight_layout()
    return fig


def plot_correlation_heatmap(df: pd.DataFrame) -> plt.Figure | None:
    """
    Correlation heatmap for numeric columns (only if ≥ 3 numeric columns exist).
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 3:
        return None

    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_SQUARE, dpi=CHART_DPI)
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("Numeric Feature Correlations", fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    return fig


def plot_distribution(df: pd.DataFrame, column: str) -> plt.Figure | None:
    """
    Histogram + KDE for a single numeric column.
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return None

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_SQUARE, dpi=CHART_DPI)
    sns.histplot(df[column].dropna(), kde=True, color=CHART_PALETTE[1], ax=ax, bins=25)
    ax.set_title(f"Distribution of {column}", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(column, fontsize=11)
    ax.set_ylabel("Count", fontsize=11)
    _style_axes(ax)
    fig.tight_layout()
    return fig


# ── Private helpers ───────────────────────────────────────────────────────────

def _style_axes(ax: plt.Axes) -> None:
    """Apply a consistent, clean look to any Axes object."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=9)
    ax.grid(axis="y", alpha=0.35, linestyle="--")
