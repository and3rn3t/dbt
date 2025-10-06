"""Tests for utility functions."""

from pathlib import Path

import pandas as pd
import pytest

from scripts.utils import (
    DATA_DIR,
    PROJECT_ROOT,
    get_data_path,
    load_csv,
    save_csv,
    validate_dataframe,
)


def test_project_root_exists():
    """Test that PROJECT_ROOT points to valid directory."""
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()


def test_data_dir_exists():
    """Test that DATA_DIR exists."""
    assert DATA_DIR.exists()
    assert DATA_DIR.is_dir()


def test_get_data_path_without_filename():
    """Test get_data_path returns correct directory path."""
    path = get_data_path("raw")
    assert path == DATA_DIR / "raw"
    assert path.exists()


def test_get_data_path_with_filename():
    """Test get_data_path returns correct file path."""
    path = get_data_path("raw", "test.csv")
    assert path == DATA_DIR / "raw" / "test.csv"


def test_validate_dataframe_empty():
    """Test validation fails for empty DataFrame."""
    df = pd.DataFrame()
    with pytest.raises(AssertionError, match="DataFrame is empty"):
        validate_dataframe(df)


def test_validate_dataframe_missing_columns():
    """Test validation fails for missing required columns."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    with pytest.raises(AssertionError, match="Missing required columns"):
        validate_dataframe(df, required_columns=["a", "b"])


def test_validate_dataframe_success():
    """Test validation passes for valid DataFrame."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    # Should not raise any exception
    validate_dataframe(df, required_columns=["a", "b"])


def test_validate_dataframe_with_nulls(capsys):
    """Test validation warns about null values."""
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})
    validate_dataframe(df)
    captured = capsys.readouterr()
    assert "Warning: Null values found" in captured.out
