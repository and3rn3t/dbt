"""
Fetch Iowa state-level Census data for comparison with Scott County.

This script fetches the same Census variables at the state level to enable
state vs. county comparisons.
"""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
STATE_FIPS = "19"  # Iowa

# Same datasets as Scott County for comparison
CENSUS_DATASETS = {
    "education": {
        "variables": [
            "B15003_001E",  # Total population 25+
            "B15003_022E",  # Bachelor's degree
            "B15003_023E",  # Master's degree
            "B15003_024E",  # Professional degree
            "B15003_025E",  # Doctorate degree
        ],
        "description": "Educational attainment for population 25 years and over",
    },
    "income": {
        "variables": [
            "B19013_001E",  # Median household income
            "B19301_001E",  # Per capita income
            "B17001_002E",  # Income below poverty level
            "B17001_001E",  # Total for poverty status
            "B19001_001E",  # Total households
        ],
        "description": "Income and poverty statistics",
    },
    "demographics": {
        "variables": [
            "B01003_001E",  # Total population
            "B01002_001E",  # Median age
            "B02001_002E",  # White alone
            "B02001_003E",  # Black/African American alone
            "B03003_003E",  # Hispanic or Latino
            "B01001_003E",  # Male under 5
            "B01001_027E",  # Female under 5
        ],
        "description": "Population and demographic characteristics",
    },
    "housing": {
        "variables": [
            "B25077_001E",  # Median home value
            "B25064_001E",  # Median gross rent
            "B25003_001E",  # Total occupied housing units
            "B25003_002E",  # Owner occupied
            "B25003_003E",  # Renter occupied
        ],
        "description": "Housing characteristics",
    },
    "employment": {
        "variables": [
            "B23025_001E",  # Total population 16+
            "B23025_002E",  # In labor force
            "B23025_004E",  # Employed
            "B23025_005E",  # Unemployed
        ],
        "description": "Employment status",
    },
}


def fetch_state_data(year: int = 2021) -> dict:
    """
    Fetch Iowa state-level data for all datasets.

    Args:
        year: Year to fetch data for (default 2021)

    Returns:
        Dictionary with dataset names as keys and DataFrames as values
    """
    print(f"\n{'='*80}")
    print(f"FETCHING IOWA STATE DATA - {year}")
    print(f"{'='*80}\n")

    results = {}

    for dataset_name, config in CENSUS_DATASETS.items():
        print(f"\nFetching {dataset_name}...")
        print(f"Description: {config['description']}")

        # Build variables list
        variables = ",".join(config["variables"])

        # Build API URL for state-level data
        url = (
            f"https://api.census.gov/data/{year}/acs/acs5"
            f"?get=NAME,{variables}"
            f"&for=state:{STATE_FIPS}"
        )

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            df["year"] = year

            # Calculate metrics
            df = calculate_metrics(df, dataset_name)

            results[dataset_name] = df

            print(f"  ✓ Successfully fetched {len(df)} row")

        except Exception as e:
            print(f"  ✗ Error fetching {dataset_name}: {e}")
            continue

    return results


def calculate_metrics(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Calculate derived metrics and percentages."""

    # Convert numeric columns
    for col in df.columns:
        if col not in ["NAME", "state", "year"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if dataset_name == "education":
        total_pop = df["B15003_001E"]
        bachelors_plus = (
            df["B15003_022E"]
            + df["B15003_023E"]
            + df["B15003_024E"]
            + df["B15003_025E"]
        )
        df["bachelors_plus_pct"] = (bachelors_plus / total_pop * 100).round(1)

    elif dataset_name == "income":
        df["poverty_rate_pct"] = (df["B17001_002E"] / df["B17001_001E"] * 100).round(1)

    elif dataset_name == "demographics":
        total_pop = df["B01003_001E"]
        df["white_pct"] = (df["B02001_002E"] / total_pop * 100).round(1)
        df["black_pct"] = (df["B02001_003E"] / total_pop * 100).round(1)
        df["hispanic_pct"] = (df["B03003_003E"] / total_pop * 100).round(1)
        df["under_5_total"] = df["B01001_003E"] + df["B01001_027E"]

    elif dataset_name == "housing":
        total_units = df["B25003_001E"]
        df["owner_occupied_pct"] = (df["B25003_002E"] / total_units * 100).round(1)
        df["renter_occupied_pct"] = (df["B25003_003E"] / total_units * 100).round(1)

    elif dataset_name == "employment":
        pop_16_plus = df["B23025_001E"]
        labor_force = df["B23025_002E"]
        df["labor_force_participation_pct"] = (labor_force / pop_16_plus * 100).round(1)
        df["unemployment_rate_pct"] = (df["B23025_005E"] / labor_force * 100).round(1)

    return df


def fetch_historical_state_data(start_year: int = 2009, end_year: int = 2021) -> dict:
    """
    Fetch historical Iowa state data for trend analysis.

    Args:
        start_year: First year to fetch
        end_year: Last year to fetch

    Returns:
        Dictionary with dataset names as keys and DataFrames as values
    """
    print(f"\n{'='*80}")
    print(f"FETCHING IOWA STATE HISTORICAL DATA ({start_year}-{end_year})")
    print(f"{'='*80}\n")

    all_results = {}

    for dataset_name in CENSUS_DATASETS.keys():
        print(f"\nFetching {dataset_name} historical data...")
        dataset_frames = []

        for year in range(start_year, end_year + 1):
            try:
                year_data = fetch_state_data_single(dataset_name, year)
                if year_data is not None:
                    dataset_frames.append(year_data)
                    print(f"  ✓ {year}")
            except Exception as e:
                print(f"  ✗ {year}: {e}")
                continue

        if dataset_frames:
            combined_df = pd.concat(dataset_frames, ignore_index=True)
            combined_df = combined_df.sort_values("year")
            all_results[dataset_name] = combined_df
            print(f"\n  Total: {len(combined_df)} years of data")
        else:
            print(f"\n  No data collected for {dataset_name}")

    return all_results


def fetch_state_data_single(dataset_name: str, year: int) -> pd.DataFrame:
    """Fetch single dataset for single year."""
    config = CENSUS_DATASETS[dataset_name]
    variables = ",".join(config["variables"])

    url = (
        f"https://api.census.gov/data/{year}/acs/acs5"
        f"?get=NAME,{variables}"
        f"&for=state:{STATE_FIPS}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df["year"] = year

    return calculate_metrics(df, dataset_name)


def save_results(results: dict, prefix: str = "current"):
    """Save results to CSV files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'='*80}")
    print("SAVING FILES")
    print(f"{'='*80}\n")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for dataset_name, df in results.items():
        filename = f"iowa_state_{dataset_name}_{prefix}_{timestamp}.csv"
        filepath = DATA_DIR / filename
        df.to_csv(filepath, index=False)
        print(f"  ✓ Saved: {filename}")

    print(f"\nAll files saved to: {DATA_DIR}")


def main():
    """Main execution function."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "historical":
        # Fetch historical data
        results = fetch_historical_state_data()
        if results:
            save_results(results, prefix="historical")
            print("\n✓ Historical Iowa state data fetched successfully!")
    else:
        # Fetch current year data
        results = fetch_state_data(year=2021)
        if results:
            save_results(results, prefix="2021")
            print("\n✓ Current Iowa state data (2021) fetched successfully!")

    print("\nNext steps:")
    print("  1. Run comparison: python scripts/compare_county_to_state.py")
    print("  2. Analyze trends: python scripts/analyze_yoy_changes.py")


if __name__ == "__main__":
    main()
    main()
    main()
    main()
    main()
