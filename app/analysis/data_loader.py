"""
analysis/data_loader.py — Responsible for reading and validating CSV uploads.

Keeps all I/O and schema-detection logic in one place so the rest of
the application works with clean, typed DataFrames.
"""

import io
import pandas as pd
from typing import Optional


def load_csv(source) -> pd.DataFrame:
    """
    Load a CSV from a file path string OR a Streamlit UploadedFile object.

    Args:
        source: Either a file-system path (str) or a Streamlit UploadedFile.

    Returns:
        A pandas DataFrame with basic type inference applied.

    Raises:
        ValueError: If the file cannot be parsed as a valid CSV.
    """
    try:
        if isinstance(source, str):
            df = pd.read_csv(source)
        else:
            # Streamlit UploadedFile is file-like; wrap bytes for safety
            content = source.read()
            df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise ValueError(f"Could not parse CSV: {exc}") from exc

    if df.empty:
        raise ValueError("The uploaded file contains no data.")

    # Attempt to parse any column with 'date' in its name as datetime
    df = _coerce_date_columns(df)
    return df


def _coerce_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Automatically detect and convert date-like string columns."""
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass  # Leave column as-is if conversion fails
    return df


def get_column_types(df: pd.DataFrame) -> dict[str, list[str]]:
    """
    Classify columns into numeric, categorical, and datetime buckets.

    Returns:
        Dict with keys 'numeric', 'categorical', 'datetime'.
    """
    result: dict[str, list[str]] = {"numeric": [], "categorical": [], "datetime": []}

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            result["datetime"].append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            result["numeric"].append(col)
        else:
            result["categorical"].append(col)

    return result


def get_preview(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return the first n rows for display."""
    return df.head(n)
