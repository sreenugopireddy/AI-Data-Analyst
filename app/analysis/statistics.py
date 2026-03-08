"""
analysis/statistics.py — Generates descriptive statistics from a DataFrame.

Produces both human-readable summaries (for the LLM prompt) and
structured dicts (for the UI).
"""

import pandas as pd
from analysis.data_loader import get_column_types


def compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return pandas' describe() for all numeric columns, transposed for readability.
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.describe().T.round(2)


def compute_category_stats(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    For each categorical column, compute value_counts as a small table.

    Returns a dict mapping column_name → value counts DataFrame.
    """
    col_types = get_column_types(df)
    stats: dict[str, pd.DataFrame] = {}

    for col in col_types["categorical"]:
        counts = df[col].value_counts().reset_index()
        counts.columns = [col, "count"]
        stats[col] = counts.head(10)   # Cap at top-10 to keep prompts concise

    return stats


def compute_revenue_trend(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Attempt to build a monthly revenue trend.

    Looks for a datetime column and a 'revenue' or numeric column to aggregate.
    Returns a DataFrame with columns [period, revenue] or None if not possible.
    """
    col_types = get_column_types(df)

    if not col_types["datetime"]:
        return None

    date_col = col_types["datetime"][0]

    # Find the most likely revenue column
    revenue_col = _find_column(df, ["revenue", "sales", "amount", "total", "price"])
    if revenue_col is None and col_types["numeric"]:
        revenue_col = col_types["numeric"][0]
    if revenue_col is None:
        return None

    trend = (
        df.groupby(df[date_col].dt.to_period("M"))[revenue_col]
        .sum()
        .reset_index()
    )
    trend.columns = ["period", "revenue"]
    trend["period"] = trend["period"].astype(str)
    return trend


def build_stats_summary_for_llm(df: pd.DataFrame) -> str:
    """
    Produce a compact, text-friendly statistics block for the LLM prompt.
    """
    lines: list[str] = []

    # Numeric summary
    desc = compute_descriptive_stats(df)
    if not desc.empty:
        lines.append("=== Numeric Column Statistics ===")
        lines.append(desc.to_string())

    # Category breakdown
    cat_stats = compute_category_stats(df)
    if cat_stats:
        lines.append("\n=== Categorical Column Summaries ===")
        for col, counts_df in cat_stats.items():
            lines.append(f"\n[{col}]")
            lines.append(counts_df.to_string(index=False))

    # Basic dataset health
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        lines.append("\n=== Missing Values ===")
        lines.append(missing.to_string())
    else:
        lines.append("\n=== Missing Values: None ===")

    return "\n".join(lines)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first column whose name contains any candidate substring."""
    lower_cols = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        for lower, original in lower_cols.items():
            if candidate in lower:
                return original
    return None
