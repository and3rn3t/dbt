"""
Fetch Census Data for Iowa Comparison Counties

This script fetches the same metrics as Scott County for:
- Linn County (Cedar Rapids)
- Black Hawk County (Waterloo)
- Dubuque County (Dubuque)

Usage:
    python scripts/fetch_comparison_counties.py
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import requests

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Configuration
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Iowa comparison counties
COUNTIES = {
    "linn": {"name": "Linn County", "fips": "113", "city": "Cedar Rapids"},
    "black_hawk": {"name": "Black Hawk County", "fips": "013", "city": "Waterloo"},
    "dubuque": {"name": "Dubuque County", "fips": "061", "city": "Dubuque"},
}

STATE_FIPS = "19"  # Iowa

# Census API base URL
BASE_URL = "https://api.census.gov/data"

# Years to fetch (ACS 5-year estimates)
YEARS = list(range(2009, 2022))  # 2009-2021

# Variable definitions matching Scott County structure
VARIABLE_GROUPS = {
    "demographics": {
        "B01003_001E": "total_population",
        "B01002_001E": "median_age",
    },
    "income": {
        "B19013_001E": "median_household_income",
        "B19301_001E": "per_capita_income",
        "B17001_002E": "population_below_poverty",
        "B17001_001E": "population_poverty_determined",
    },
    "education": {
        "B15003_022E": "bachelor_degree",
        "B15003_023E": "master_degree",
        "B15003_024E": "professional_degree",
        "B15003_025E": "doctorate_degree",
        "B15003_001E": "total_25_plus_population",
    },
    "employment": {
        "B23025_005E": "unemployed",
        "B23025_003E": "labor_force",
    },
    "housing": {
        "B25077_001E": "median_home_value",
        "B25064_001E": "median_gross_rent",
    },
}


def get_census_api_key() -> Optional[str]:
    """Get Census API key from environment."""
    api_key = os.getenv("CENSUS_API_KEY")
    if not api_key:
        print("⚠️  Warning: CENSUS_API_KEY not found in environment")
        print(
            "   You can get a free key at: https://api.census.gov/data/key_signup.html"
        )
        print("   Set it with: $env:CENSUS_API_KEY='your_key_here'")
    return api_key


def fetch_acs_data(
    year: int,
    variables: List[str],
    state: str,
    county: str,
    api_key: Optional[str] = None,
) -> Optional[Dict]:
    """Fetch ACS 5-year estimate data for a county."""

    # Build URL
    var_string = ",".join(variables)
    url = f"{BASE_URL}/{year}/acs/acs5"

    params = {
        "get": var_string,
        "for": f"county:{county}",
        "in": f"state:{state}",
    }

    if api_key:
        params["key"] = api_key

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        if len(data) > 1:
            # First row is headers, second row is data
            headers = data[0]
            values = data[1]
            return dict(zip(headers, values))
        return None

    except requests.exceptions.RequestException as e:
        print(f"    ⚠️  Error fetching {year}: {e}")
        return None


def fetch_county_data(
    county_key: str, county_info: Dict, api_key: Optional[str] = None
) -> Dict[str, pd.DataFrame]:
    """Fetch all data categories for a county."""

    print(f"\n{'=' * 80}")
    print(f"Fetching data for {county_info['name']} ({county_info['city']})")
    print(f"{'=' * 80}\n")

    results = {}

    for category, variables in VARIABLE_GROUPS.items():
        print(f"  📊 Fetching {category}...")

        category_data = []
        var_codes = list(variables.keys())

        for year in YEARS:
            print(f"    • {year}...", end=" ")

            data = fetch_acs_data(
                year, var_codes, STATE_FIPS, county_info["fips"], api_key
            )

            if data:
                row = {"year": year}

                # Map variable codes to friendly names
                for var_code, var_name in variables.items():
                    value = data.get(var_code)
                    if value and value != "-666666666":  # Census null value
                        try:
                            row[var_name] = float(value)
                        except (ValueError, TypeError):
                            row[var_name] = None
                    else:
                        row[var_name] = None

                category_data.append(row)
                print("✓")
            else:
                print("✗")

            time.sleep(0.1)  # Be nice to the API

        if category_data:
            df = pd.DataFrame(category_data)

            # Calculate derived metrics
            if category == "income" and "population_below_poverty" in df.columns:
                df["poverty_rate_pct"] = (
                    df["population_below_poverty"]
                    / df["population_poverty_determined"]
                    * 100
                )

            if category == "employment" and "unemployed" in df.columns:
                df["unemployment_rate_pct"] = df["unemployed"] / df["labor_force"] * 100

            if category == "education":
                df["bachelor_degree_or_higher"] = (
                    df["bachelor_degree"]
                    + df["master_degree"]
                    + df["professional_degree"]
                    + df["doctorate_degree"]
                )
                df["bachelor's_degree_or_higher_pct"] = (
                    df["bachelor_degree_or_higher"]
                    / df["total_25_plus_population"]
                    * 100
                )

            results[category] = df
            print(f"    ✅ Fetched {len(df)} years of {category} data")
        else:
            print(f"    ❌ No data retrieved for {category}")

    return results


def save_county_data(
    county_key: str, county_info: Dict, data: Dict[str, pd.DataFrame]
) -> None:
    """Save county data to CSV files."""

    print(f"\n  💾 Saving {county_info['name']} data...")

    for category, df in data.items():
        filename = f"{county_key}_county_{category}_historical.csv"
        filepath = DATA_DIR / filename
        df.to_csv(filepath, index=False)
        print(f"    ✅ Saved: {filename}")


def create_unified_dataset(
    county_key: str, data: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """Create a unified time series dataset for a county."""

    print(f"\n  🔗 Creating unified time series...")

    # Start with year column
    all_years = sorted(set().union(*[set(df["year"]) for df in data.values()]))
    unified = pd.DataFrame({"year": all_years})

    # Merge each category
    for category, df in data.items():
        # Select relevant columns (exclude intermediate calculation columns)
        if category == "demographics":
            cols = ["year", "total_population", "median_age"]
        elif category == "income":
            cols = [
                "year",
                "median_household_income",
                "per_capita_income",
                "poverty_rate_pct",
            ]
        elif category == "education":
            cols = ["year", "bachelor's_degree_or_higher_pct"]
        elif category == "employment":
            cols = ["year", "unemployment_rate_pct"]
        elif category == "housing":
            cols = ["year", "median_home_value", "median_gross_rent"]
        else:
            cols = df.columns.tolist()

        # Keep only columns that exist
        cols = [c for c in cols if c in df.columns]
        subset = df[cols].copy()

        unified = unified.merge(subset, on="year", how="left")

    # Add metadata
    unified.insert(0, "state_fips", STATE_FIPS)
    unified.insert(1, "county_fips", COUNTIES[county_key]["fips"])
    unified.insert(2, "county_name", COUNTIES[county_key]["name"])

    print(
        f"    ✅ Unified dataset: {len(unified)} rows, {len(unified.columns)} columns"
    )

    return unified


def main():
    """Main execution function."""

    print("=" * 80)
    print("IOWA COMPARISON COUNTIES - CENSUS DATA FETCH")
    print("=" * 80)
    print(f"\nFetching data for {len(COUNTIES)} counties")
    print(f"Years: {min(YEARS)} - {max(YEARS)}")
    print(f"Categories: {', '.join(VARIABLE_GROUPS.keys())}")

    # Get API key
    api_key = get_census_api_key()
    if not api_key:
        print("\n⚠️  Proceeding without API key (requests may be rate-limited)")

    input("\nPress Enter to begin fetching data...")

    start_time = datetime.now()

    # Fetch data for each county
    all_unified = []

    for county_key, county_info in COUNTIES.items():
        try:
            # Fetch all categories
            data = fetch_county_data(county_key, county_info, api_key)

            if data:
                # Save individual category files
                save_county_data(county_key, county_info, data)

                # Create and save unified dataset
                unified = create_unified_dataset(county_key, data)
                unified_path = DATA_DIR / f"{county_key}_county_unified_timeseries.csv"
                unified.to_csv(unified_path, index=False)
                print(f"    ✅ Saved: {unified_path.name}")

                all_unified.append(unified)
            else:
                print(f"    ❌ Failed to fetch data for {county_info['name']}")

        except Exception as e:
            print(f"\n❌ Error processing {county_info['name']}: {e}")
            continue

    # Create master comparison file
    if all_unified:
        print(f"\n{'=' * 80}")
        print("Creating master comparison file...")
        print(f"{'=' * 80}\n")

        master_df = pd.concat(all_unified, ignore_index=True)
        master_path = DATA_DIR / "iowa_comparison_counties_unified.csv"
        master_df.to_csv(master_path, index=False)
        print(f"  ✅ Saved master file: {master_path.name}")
        print(f"     Total rows: {len(master_df):,}")
        print(f"     Counties: {master_df['county_name'].nunique()}")

    # Summary
    elapsed = datetime.now() - start_time

    print(f"\n{'=' * 80}")
    print("FETCH COMPLETE!")
    print(f"{'=' * 80}\n")
    print(f"  ⏱️  Time elapsed: {elapsed}")
    print(f"  📁 Data saved to: {DATA_DIR}")
    print(f"  ✅ Counties fetched: {len(all_unified)} of {len(COUNTIES)}")

    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("\n1. Run the iowa_cities_comparison.ipynb notebook")
    print("2. The notebook will automatically load the fetched data")
    print("3. All visualizations will use real Census data")
    print("\n💡 Tip: Save your CENSUS_API_KEY to .env file for future use")


if __name__ == "__main__":
    main()
