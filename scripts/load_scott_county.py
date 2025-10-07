"""
Scott County Data Loader

Utility functions for loading cleaned Scott County Census data.

Usage:
    from scripts.load_scott_county import load_unified, load_historical, load_snapshot

    # Load unified time series
    df = load_unified()

    # Load specific historical data
    income_df = load_historical('income')

    # Load 2021 snapshot
    demographics_df = load_snapshot('demographics')
"""

from pathlib import Path
from typing import Literal, Optional

import pandas as pd

# Path configuration
PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_unified() -> pd.DataFrame:
    """Load the unified time series dataset.

    Returns:
        DataFrame with 13 years of data (2009-2021) across all categories

    Example:
        >>> df = load_unified()
        >>> print(df.columns)
        >>> print(f"Years covered: {df['year'].min()} - {df['year'].max()}")
    """
    filepath = PROCESSED_DIR / "scott_county_unified_timeseries.csv"

    if not filepath.exists():
        raise FileNotFoundError(
            f"Unified dataset not found at {filepath}. "
            "Run the scott_county_data_cleaning.ipynb notebook first."
        )

    df = pd.read_csv(filepath)

    # Ensure year is integer
    if "year" in df.columns:
        df["year"] = df["year"].astype(int)

    return df


def load_historical(
    category: Literal["income", "education", "employment", "housing", "demographics"],
) -> pd.DataFrame:
    """Load a specific historical dataset (2009-2021 or subset).

    Args:
        category: One of 'income', 'education', 'employment', 'housing', 'demographics'

    Returns:
        DataFrame with historical data for the specified category

    Example:
        >>> income_df = load_historical('income')
        >>> print(income_df[['year', 'median_household_income']].head())
    """
    filename = f"scott_county_{category}_historical_cleaned.csv"
    filepath = PROCESSED_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(
            f"Historical {category} dataset not found at {filepath}. "
            "Run the scott_county_data_cleaning.ipynb notebook first."
        )

    df = pd.read_csv(filepath)

    # Ensure year is integer if present
    if "year" in df.columns:
        df["year"] = df["year"].astype(int)

    return df


def load_snapshot(
    category: Literal["income", "education", "employment", "housing", "demographics"],
) -> pd.DataFrame:
    """Load a 2021 snapshot dataset with detailed columns.

    Args:
        category: One of 'income', 'education', 'employment', 'housing', 'demographics'

    Returns:
        DataFrame with 2021 snapshot data (1 row, many columns)

    Example:
        >>> demo_df = load_snapshot('demographics')
        >>> print(f"Available columns: {len(demo_df.columns)}")
    """
    filename = f"scott_county_{category}_2021_cleaned.csv"
    filepath = PROCESSED_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(
            f"2021 snapshot {category} dataset not found at {filepath}. "
            "Run the scott_county_data_cleaning.ipynb notebook first."
        )

    df = pd.read_csv(filepath)

    return df


def load_all_historical() -> dict[str, pd.DataFrame]:
    """Load all historical datasets.

    Returns:
        Dictionary with category names as keys and DataFrames as values

    Example:
        >>> all_data = load_all_historical()
        >>> print(all_data.keys())
        >>> print(all_data['income'].head())
    """
    categories = ["income", "education", "employment", "housing", "demographics"]

    datasets = {}
    for category in categories:
        try:
            datasets[category] = load_historical(category)
        except FileNotFoundError as e:
            print(f"Warning: Could not load {category} - {e}")

    return datasets


def get_income_growth(start_year: int = 2009, end_year: int = 2021) -> dict:
    """Calculate income growth statistics.

    Args:
        start_year: Starting year for calculation (default: 2009)
        end_year: Ending year for calculation (default: 2021)

    Returns:
        Dictionary with income growth statistics

    Example:
        >>> growth = get_income_growth()
        >>> print(f"Total growth: ${growth['total_growth']:,.0f}")
        >>> print(f"Percent growth: {growth['pct_growth']:.1f}%")
    """
    df = load_unified()

    # Filter to specified years
    start_data = df[df["year"] == start_year]
    end_data = df[df["year"] == end_year]

    if start_data.empty or end_data.empty:
        raise ValueError(f"Data not available for years {start_year} or {end_year}")

    start_income = start_data["median_household_income"].iloc[0]
    end_income = end_data["median_household_income"].iloc[0]

    total_growth = end_income - start_income
    pct_growth = (total_growth / start_income) * 100
    years = end_year - start_year
    annual_growth = pct_growth / years

    return {
        "start_year": start_year,
        "end_year": end_year,
        "start_income": start_income,
        "end_income": end_income,
        "total_growth": total_growth,
        "pct_growth": pct_growth,
        "years": years,
        "annual_growth_pct": annual_growth,
    }


def get_latest_stats() -> dict:
    """Get the latest (2021) statistics summary.

    Returns:
        Dictionary with key 2021 statistics

    Example:
        >>> stats = get_latest_stats()
        >>> print(f"Population: {stats['population']:,}")
        >>> print(f"Median Income: ${stats['median_income']:,}")
    """
    df = load_unified()
    latest = df[df["year"] == 2021].iloc[0]

    return {
        "year": 2021,
        "population": int(latest["total_population"]),
        "median_age": float(latest["median_age"]),
        "median_income": int(latest["median_household_income"]),
        "per_capita_income": int(latest["per_capita_income"]),
        "poverty_rate": float(latest["poverty_rate_pct"]),
        "unemployment_rate": float(latest["unemployment_rate_pct"]),
        "bachelors_or_higher_pct": float(latest["bachelor's_degree_or_higher_pct"]),
        "median_home_value": int(latest["median_home_value"]),
        "median_rent": int(latest["median_gross_rent"]),
    }


def compare_to_iowa_state(year: int = 2021) -> pd.DataFrame:
    """Load both Scott County and Iowa state data for comparison.

    Note: Requires Iowa state data to be available in processed directory.

    Args:
        year: Year for comparison (default: 2021)

    Returns:
        DataFrame with comparison metrics

    Example:
        >>> comparison = compare_to_iowa_state(2021)
        >>> print(comparison)
    """
    # Load Scott County data
    scott_df = load_unified()
    scott_data = scott_df[scott_df["year"] == year].iloc[0]

    # Try to load Iowa state data
    iowa_files = list(PROCESSED_DIR.glob("iowa_state_*_cleaned.csv"))

    if not iowa_files:
        print("Warning: Iowa state data not found. Cannot create comparison.")
        return None

    # This is a placeholder - actual implementation would depend on Iowa data structure
    comparison = pd.DataFrame(
        {
            "Metric": [
                "Median Household Income",
                "Poverty Rate (%)",
                "Unemployment Rate (%)",
                "Bachelor's Degree or Higher (%)",
                "Median Home Value",
            ],
            "Scott County": [
                scott_data["median_household_income"],
                scott_data["poverty_rate_pct"],
                scott_data["unemployment_rate_pct"],
                scott_data["bachelor's_degree_or_higher_pct"],
                scott_data["median_home_value"],
            ],
        }
    )

    return comparison


# Quick summary function
def print_summary():
    """Print a quick summary of Scott County data."""
    print("=" * 70)
    print("SCOTT COUNTY, IOWA - DATA SUMMARY")
    print("=" * 70)

    try:
        df = load_unified()
        print(f"\n📊 Unified Time Series Dataset:")
        print(f"   Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"   Total rows: {len(df)}")
        print(f"   Total columns: {len(df.columns)}")

        stats = get_latest_stats()
        print(f"\n📈 Latest Statistics (2021):")
        print(f"   Population: {stats['population']:,}")
        print(f"   Median Age: {stats['median_age']:.1f} years")
        print(f"   Median Household Income: ${stats['median_income']:,}")
        print(f"   Poverty Rate: {stats['poverty_rate']:.1f}%")
        print(f"   Unemployment Rate: {stats['unemployment_rate']:.1f}%")
        print(
            f"   Bachelor's Degree or Higher: {stats['bachelors_or_higher_pct']:.1f}%"
        )
        print(f"   Median Home Value: ${stats['median_home_value']:,}")

        growth = get_income_growth()
        print(f"\n💰 Income Growth (2009-2021):")
        print(f"   Starting Income: ${growth['start_income']:,}")
        print(f"   Ending Income: ${growth['end_income']:,}")
        print(
            f"   Total Growth: ${growth['total_growth']:,} ({growth['pct_growth']:.1f}%)"
        )
        print(f"   Average Annual Growth: {growth['annual_growth_pct']:.2f}%/year")

        print("\n" + "=" * 70)
        print("✅ Data ready for analysis!")
        print("=" * 70)

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease run the scott_county_data_cleaning.ipynb notebook first.")


if __name__ == "__main__":
    # Print summary when run as script
    print_summary()
