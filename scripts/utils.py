"""Common utility functions for data processing."""

from pathlib import Path
from typing import Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def get_data_path(subfolder: str = "raw", filename: Optional[str] = None) -> Path:
    """Get the path to a data file.

    Args:
        subfolder: Data subfolder (raw, processed, staging, external)
        filename: Optional filename to append to path

    Returns:
        Path object to the data directory or file

    Example:
        >>> path = get_data_path("raw", "data.csv")
        >>> df = pd.read_csv(path)
    """
    path = DATA_DIR / subfolder
    if filename:
        path = path / filename
    return path


def load_csv(filename: str, subfolder: str = "raw", **kwargs) -> pd.DataFrame:
    """Load a CSV file from the data directory.

    Args:
        filename: Name of the CSV file
        subfolder: Data subfolder (raw, processed, staging, external)
        **kwargs: Additional arguments to pass to pd.read_csv

    Returns:
        DataFrame with the loaded data

    Example:
        >>> df = load_csv("sample_sales_data.csv")
    """
    filepath = get_data_path(subfolder, filename)
    return pd.read_csv(filepath, **kwargs)


def save_csv(
    df: pd.DataFrame, filename: str, subfolder: str = "processed", **kwargs
) -> Path:
    """Save a DataFrame to CSV in the data directory.

    Args:
        df: DataFrame to save
        filename: Name of the CSV file
        subfolder: Data subfolder (raw, processed, staging, external)
        **kwargs: Additional arguments to pass to df.to_csv

    Returns:
        Path to the saved file

    Example:
        >>> save_csv(df, "cleaned_data.csv", index=False)
    """
    filepath = get_data_path(subfolder, filename)
    df.to_csv(filepath, **kwargs)
    return filepath


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[list[str]] = None,
    check_nulls: bool = True,
) -> None:
    """Validate a DataFrame meets basic requirements.

    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        check_nulls: Whether to check for null values

    Raises:
        AssertionError: If validation fails

    Example:
        >>> validate_dataframe(df, required_columns=["id", "name"])
    """
    assert not df.empty, "DataFrame is empty"

    if required_columns:
        missing = set(required_columns) - set(df.columns)
        assert not missing, f"Missing required columns: {missing}"

    if check_nulls:
        nulls = df.isnull().sum()
        if nulls.any():
            print("Warning: Null values found:")
            print(nulls[nulls > 0])
