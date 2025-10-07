#!/usr/bin/env python3
"""
Fetch historical Census data for Scott County, Iowa.

This script fetches data for all available years to show trends over time.

ACS 5-Year Estimates available:
- 2009-2021 (13 years of comprehensive data)

Usage:
    python scripts/fetch_scott_county_historical.py
    python scripts/fetch_scott_county_historical.py --start-year 2015
    python scripts/fetch_scott_county_historical.py --dataset education
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Scott County, Iowa identifiers
STATE_FIPS = "19"  # Iowa
COUNTY_FIPS = "163"  # Scott County
LOCATION_NAME = "Scott County, Iowa"

# Available years (ACS 5-Year Estimates)
AVAILABLE_YEARS = list(range(2009, 2022))  # 2009-2021

# Simplified datasets for historical analysis
CENSUS_DATASETS = {
    "education": {
        "name": "Educational Attainment",
        "variables": {
            "B15003_001E": "Total population 25 years and over",
            "B15003_017E": "High school graduate",
            "B15003_021E": "Bachelor's degree",
            "B15003_022E": "Master's degree",
            "B15003_023E": "Professional school degree",
            "B15003_024E": "Doctorate degree",
        },
    },
    "income": {
        "name": "Income and Poverty",
        "variables": {
            "B19013_001E": "Median household income",
            "B19301_001E": "Per capita income",
            "B17001_001E": "Population for whom poverty status is determined",
            "B17001_002E": "Income below poverty level",
        },
    },
    "demographics": {
        "name": "Demographics",
        "variables": {
            "B01001_001E": "Total population",
            "B01002_001E": "Median age",
            "B02001_002E": "White alone",
            "B02001_003E": "Black or African American alone",
            "B02001_005E": "Asian alone",
            "B03001_003E": "Hispanic or Latino",
        },
    },
    "housing": {
        "name": "Housing",
        "variables": {
            "B25001_001E": "Total housing units",
            "B25003_002E": "Owner occupied",
            "B25003_003E": "Renter occupied",
            "B25077_001E": "Median home value",
            "B25064_001E": "Median gross rent",
        },
    },
    "employment": {
        "name": "Employment",
        "variables": {
            "B23025_003E": "Civilian labor force",
            "B23025_004E": "Employed",
            "B23025_005E": "Unemployed",
        },
    },
}


def check_api_key():
    """Check if Census API key is available."""
    api_key = os.getenv("CENSUS_API_KEY")

    if not api_key:
        print("\nℹ️  No Census API key (optional - will work without it)")
        return None

    if len(api_key) < 30:
        print("\n⚠️  Census API key looks invalid")
        return None

    return api_key


def fetch_year_data(dataset_name, dataset_info, year):
    """Fetch data for a specific year."""
    api_key = check_api_key()

    variables = dataset_info["variables"]
    var_list = ",".join(variables.keys())

    base_url = f"https://api.census.gov/data/{year}/acs/acs5"

    params = {
        "get": f"NAME,{var_list}",
        "for": f"county:{COUNTY_FIPS}",
        "in": f"state:{STATE_FIPS}",
    }

    if api_key:
        params["key"] = api_key

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()

        # Check for HTML error response
        if response.text.startswith("<"):
            return None

        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Add year column
        df["year"] = year

        # Rename columns
        for var_code, var_name in variables.items():
            if var_code in df.columns:
                df.rename(columns={var_code: var_name}, inplace=True)

        # Convert numeric columns
        for col in df.columns:
            if col not in ["NAME", "state", "county", "year"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


def calculate_metrics(df, dataset_name):
    """Calculate percentages and derived metrics."""

    if dataset_name == "education":
        total_col = "Total population 25 years and over"
        if total_col in df.columns:
            # Bachelor's or higher
            bachelor_cols = [
                "Bachelor's degree",
                "Master's degree",
                "Professional school degree",
                "Doctorate degree",
            ]
            available = [col for col in bachelor_cols if col in df.columns]
            if available:
                df["Bachelor's degree or higher"] = df[available].sum(axis=1)
                df["Bachelor's degree or higher (%)"] = (
                    df["Bachelor's degree or higher"] / df[total_col] * 100
                ).round(2)

            # High school graduate %
            if "High school graduate" in df.columns:
                df["High school graduate (%)"] = (
                    df["High school graduate"] / df[total_col] * 100
                ).round(2)

    elif dataset_name == "income":
        if "Population for whom poverty status is determined" in df.columns:
            if "Income below poverty level" in df.columns:
                df["Poverty rate (%)"] = (
                    df["Income below poverty level"]
                    / df["Population for whom poverty status is determined"]
                    * 100
                ).round(2)

    elif dataset_name == "demographics":
        if "Total population" in df.columns:
            race_cols = [
                "White alone",
                "Black or African American alone",
                "Asian alone",
                "Hispanic or Latino",
            ]
            for col in race_cols:
                if col in df.columns:
                    df[f"{col} (%)"] = (df[col] / df["Total population"] * 100).round(2)

    elif dataset_name == "housing":
        if "Owner occupied" in df.columns and "Renter occupied" in df.columns:
            total = df["Owner occupied"] + df["Renter occupied"]
            df["Owner occupied (%)"] = (df["Owner occupied"] / total * 100).round(2)

    elif dataset_name == "employment":
        if "Civilian labor force" in df.columns and "Unemployed" in df.columns:
            df["Unemployment rate (%)"] = (
                df["Unemployed"] / df["Civilian labor force"] * 100
            ).round(2)

    return df


def fetch_historical_dataset(dataset_name, dataset_info, start_year, end_year):
    """Fetch historical data for all years."""
    print(f"\n{'='*80}")
    print(f"Fetching Historical: {dataset_info['name']}")
    print(f"{'='*80}")
    print(f"Location: {LOCATION_NAME}")
    print(f"Years: {start_year}-{end_year} ({end_year - start_year + 1} years)")
    print(f"Variables: {len(dataset_info['variables'])}")

    all_data = []
    failed_years = []

    for year in range(start_year, end_year + 1):
        print(f"  Fetching {year}...", end=" ", flush=True)

        df = fetch_year_data(dataset_name, dataset_info, year)

        if df is not None and not df.empty:
            df = calculate_metrics(df, dataset_name)
            all_data.append(df)
            print("✓")
        else:
            failed_years.append(year)
            print("✗")

        # Be nice to the API
        time.sleep(0.5)

    if not all_data:
        print(f"\n❌ No data retrieved")
        return None

    # Combine all years
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values("year")

    print(f"\n✓ Successfully fetched {len(all_data)} years")
    if failed_years:
        print(f"⚠ Failed years: {', '.join(map(str, failed_years))}")

    return combined


def save_historical_data(df, dataset_name):
    """Save historical data to file."""
    if df is None or df.empty:
        return None

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scott_county_iowa_{dataset_name}_historical_{timestamp}.csv"
    output_file = output_dir / filename

    df.to_csv(output_file, index=False)

    file_size_kb = output_file.stat().st_size / 1024
    print(f"\n✓ Saved: {output_file.name}")
    print(f"✓ Records: {len(df)} (years × variables)")
    print(f"✓ Size: {file_size_kb:.2f} KB")

    return output_file


def show_trends(df, dataset_name):
    """Show key trends over time."""
    if df is None or df.empty:
        return

    print(f"\n{'='*80}")
    print(f"TRENDS OVER TIME: {dataset_name.upper()}")
    print(f"{'='*80}\n")

    years = sorted(df["year"].unique())
    first_year = years[0]
    last_year = years[-1]

    if dataset_name == "education":
        col = "Bachelor's degree or higher (%)"
        if col in df.columns:
            first = df[df["year"] == first_year][col].iloc[0]
            last = df[df["year"] == last_year][col].iloc[0]
            change = last - first
            print(f"📚 Bachelor's Degree or Higher:")
            print(f"   {first_year}: {first:.1f}%")
            print(f"   {last_year}: {last:.1f}%")
            print(f"   Change: {change:+.1f} percentage points")

    elif dataset_name == "income":
        col = "Median household income"
        if col in df.columns:
            first = df[df["year"] == first_year][col].iloc[0]
            last = df[df["year"] == last_year][col].iloc[0]
            pct_change = ((last - first) / first) * 100
            print(f"💰 Median Household Income:")
            print(f"   {first_year}: ${first:,.0f}")
            print(f"   {last_year}: ${last:,.0f}")
            print(f"   Change: ${last - first:+,.0f} ({pct_change:+.1f}%)")

    elif dataset_name == "demographics":
        col = "Total population"
        if col in df.columns:
            first = df[df["year"] == first_year][col].iloc[0]
            last = df[df["year"] == last_year][col].iloc[0]
            pct_change = ((last - first) / first) * 100
            print(f"👥 Total Population:")
            print(f"   {first_year}: {first:,.0f}")
            print(f"   {last_year}: {last:,.0f}")
            print(f"   Change: {last - first:+,.0f} ({pct_change:+.1f}%)")

    elif dataset_name == "housing":
        col = "Median home value"
        if col in df.columns:
            first = df[df["year"] == first_year][col].iloc[0]
            last = df[df["year"] == last_year][col].iloc[0]
            pct_change = ((last - first) / first) * 100
            print(f"🏠 Median Home Value:")
            print(f"   {first_year}: ${first:,.0f}")
            print(f"   {last_year}: ${last:,.0f}")
            print(f"   Change: ${last - first:+,.0f} ({pct_change:+.1f}%)")

    elif dataset_name == "employment":
        col = "Unemployment rate (%)"
        if col in df.columns:
            first = df[df["year"] == first_year][col].iloc[0]
            last = df[df["year"] == last_year][col].iloc[0]
            change = last - first
            print(f"💼 Unemployment Rate:")
            print(f"   {first_year}: {first:.1f}%")
            print(f"   {last_year}: {last:.1f}%")
            print(f"   Change: {change:+.1f} percentage points")

    print()


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Fetch historical Census data for Scott County, Iowa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Fetches Census data for all available years (2009-2021).

This creates historical trend datasets perfect for time series analysis.

Examples:
  # Fetch all datasets for all years
  python scripts/fetch_scott_county_historical.py

  # Just education data
  python scripts/fetch_scott_county_historical.py --dataset education

  # From 2015 onwards
  python scripts/fetch_scott_county_historical.py --start-year 2015
        """,
    )

    parser.add_argument(
        "--dataset",
        choices=list(CENSUS_DATASETS.keys()) + ["all"],
        default="all",
        help="Specific dataset to fetch (default: all)",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2009,
        help="Starting year (default: 2009, earliest available)",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2021,
        help="Ending year (default: 2021, most recent)",
    )

    args = parser.parse_args()

    # Validate years
    if args.start_year < 2009:
        print("⚠ Warning: ACS 5-Year data starts in 2009")
        args.start_year = 2009

    if args.end_year > 2021:
        print("⚠ Warning: 2021 is most recent complete year")
        args.end_year = 2021

    try:
        print("\n" + "=" * 80)
        print(f"FETCHING HISTORICAL CENSUS DATA FOR {LOCATION_NAME}")
        print("=" * 80)
        print(f"State FIPS: {STATE_FIPS} (Iowa)")
        print(f"County FIPS: {COUNTY_FIPS} (Scott County)")
        print(f"Years: {args.start_year}-{args.end_year}")
        print(f"Source: ACS 5-Year Estimates")
        print("=" * 80)

        datasets_to_fetch = (
            CENSUS_DATASETS.keys() if args.dataset == "all" else [args.dataset]
        )

        all_files = []

        for dataset_name in datasets_to_fetch:
            dataset_info = CENSUS_DATASETS[dataset_name]

            # Fetch historical data
            df = fetch_historical_dataset(
                dataset_name, dataset_info, args.start_year, args.end_year
            )

            if df is not None:
                # Save data
                output_file = save_historical_data(df, dataset_name)
                if output_file:
                    all_files.append(output_file)

                # Show trends
                show_trends(df, dataset_name)

        # Final summary
        print("=" * 80)
        print("✅ HISTORICAL DATA FETCH COMPLETE")
        print("=" * 80)
        print(f"\n📁 {len(all_files)} files saved to data/raw/")
        print("\n🎯 Next Steps:")
        print("   1. Open in Jupyter Lab for time series analysis")
        print("   2. Create trend visualizations")
        print("   3. Compare year-over-year changes")
        print("   4. Forecast future trends")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
