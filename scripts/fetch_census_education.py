#!/usr/bin/env python3
"""
Fetch education data from US Census Bureau Decennial Census.

The Decennial Census (2020 is most recent) provides detailed educational attainment
data by geography (national, state, county, tract levels).

Usage:
    python scripts/fetch_census_education.py --geography state --year 2020
    python scripts/fetch_census_education.py --geography county --state 06 --year 2020
    python scripts/fetch_census_education.py --help

Notes:
    - Requires Census API key (free): https://api.census.gov/data/key_signup.html
    - Add to .env: CENSUS_API_KEY=your_key_here
    - 2020 Decennial Census is most recent
    - Educational attainment is from ACS (American Community Survey), not pure Decennial
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# State FIPS codes for reference
STATE_FIPS = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
    "72": "Puerto Rico",
}

# Educational Attainment Variables (ACS 5-Year Estimates)
# These are the most comprehensive education variables available
EDUCATION_VARIABLES = {
    "B15003_001E": "Total population 25 years and over",
    "B15003_002E": "No schooling completed",
    "B15003_003E": "Nursery school",
    "B15003_004E": "Kindergarten",
    "B15003_005E": "1st grade",
    "B15003_006E": "2nd grade",
    "B15003_007E": "3rd grade",
    "B15003_008E": "4th grade",
    "B15003_009E": "5th grade",
    "B15003_010E": "6th grade",
    "B15003_011E": "7th grade",
    "B15003_012E": "8th grade",
    "B15003_013E": "9th grade",
    "B15003_014E": "10th grade",
    "B15003_015E": "11th grade",
    "B15003_016E": "12th grade, no diploma",
    "B15003_017E": "High school graduate (includes equivalency)",
    "B15003_018E": "Some college, less than 1 year",
    "B15003_019E": "Some college, 1 or more years, no degree",
    "B15003_020E": "Associate's degree",
    "B15003_021E": "Bachelor's degree",
    "B15003_022E": "Master's degree",
    "B15003_023E": "Professional school degree",
    "B15003_024E": "Doctorate degree",
    "B15003_025E": "Graduate or professional degree",
}

# Simplified educational attainment (summary variables)
EDUCATION_SUMMARY = {
    "B15002_001E": "Total population 25 years and over",
    "B15002_011E": "Male: High school graduate",
    "B15002_012E": "Male: Some college or associate's degree",
    "B15002_015E": "Male: Bachelor's degree",
    "B15002_016E": "Male: Master's degree",
    "B15002_017E": "Male: Professional school degree",
    "B15002_018E": "Male: Doctorate degree",
    "B15002_028E": "Female: High school graduate",
    "B15002_029E": "Female: Some college or associate's degree",
    "B15002_032E": "Female: Bachelor's degree",
    "B15002_033E": "Female: Master's degree",
    "B15002_034E": "Female: Professional school degree",
    "B15002_035E": "Female: Doctorate degree",
}


def check_api_key():
    """Check if Census API key is available."""
    api_key = os.getenv("CENSUS_API_KEY")

    if not api_key:
        print("\n" + "=" * 80)
        print("⚠️  CENSUS API KEY REQUIRED")
        print("=" * 80)
        print("\nThe Census Bureau API requires a free API key.")
        print("\n📝 How to get your key:")
        print("   1. Visit: https://api.census.gov/data/key_signup.html")
        print("   2. Fill out the simple form")
        print("   3. Check your email for the key (instant)")
        print("   4. Add to your .env file:")
        print("      CENSUS_API_KEY=your_key_here")
        print("\n💡 Takes less than 2 minutes!\n")
        return None

    return api_key


def fetch_acs_education(geography, year=2021, state=None, detailed=False):
    """
    Fetch educational attainment data from Census ACS.

    Args:
        geography: 'us', 'state', 'county', 'tract'
        year: Year for ACS 5-year estimates (2021 is most recent)
        state: State FIPS code (required for county/tract)
        detailed: Use detailed variables (25 categories) vs summary (14 categories)

    Returns:
        pandas DataFrame with education data
    """
    api_key = check_api_key()
    if not api_key:
        return None

    # Select variable set
    variables = EDUCATION_VARIABLES if detailed else EDUCATION_SUMMARY
    var_list = ",".join(variables.keys())

    # Build API URL based on geography
    base_url = f"https://api.census.gov/data/{year}/acs/acs5"

    # Build geography string
    if geography == "us":
        geo_str = "us:*"
        geo_name = "United States"
    elif geography == "state":
        geo_str = "state:*"
        geo_name = "All States"
    elif geography == "county":
        if not state:
            print("❌ Error: --state required for county geography")
            return None
        geo_str = f"county:*&in=state:{state}"
        geo_name = f"Counties in {STATE_FIPS.get(state, state)}"
    elif geography == "tract":
        if not state:
            print("❌ Error: --state required for tract geography")
            return None
        geo_str = f"tract:*&in=state:{state}"
        geo_name = f"Census Tracts in {STATE_FIPS.get(state, state)}"
    else:
        print(f"❌ Error: Invalid geography '{geography}'")
        return None

    print("\n" + "=" * 80)
    print("FETCHING CENSUS EDUCATION DATA")
    print("=" * 80)
    print(f"Dataset: American Community Survey (ACS) {year} 5-Year Estimates")
    print(f"Geography: {geo_name}")
    print(f"Variables: {len(variables)} education indicators")
    print(
        f"Detail Level: {'Detailed (25 categories)' if detailed else 'Summary (14 categories)'}"
    )
    print("=" * 80 + "\n")

    # Build request URL
    params = {
        "get": f"NAME,{var_list}",
        "for": geo_str.split("&in=")[0].replace("for=", ""),
        "key": api_key,
    }

    if "&in=" in geo_str:
        params["in"] = geo_str.split("&in=")[1]

    try:
        print("Downloading data from Census Bureau API...")
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Rename columns to human-readable names
        for var_code, var_name in variables.items():
            if var_code in df.columns:
                df.rename(columns={var_code: var_name}, inplace=True)

        # Convert numeric columns
        for col in df.columns:
            if col not in ["NAME", "state", "county", "tract"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        print(f"✓ Downloaded {len(df):,} geographic areas")
        print(f"✓ Columns: {len(df.columns)}")

        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {str(e)}")
        if hasattr(e.response, "text"):
            print(f"   API Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error processing data: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def calculate_education_metrics(df):
    """Calculate useful education metrics from the raw data."""
    print("\nCalculating education metrics...")

    # Identify numeric columns (exclude geographic identifiers)
    exclude_cols = ["NAME", "state", "county", "tract"]
    numeric_cols = [col for col in df.columns if col not in exclude_cols]

    # Calculate percentages if we have total population
    total_col = next((col for col in numeric_cols if "Total population" in col), None)

    if total_col and len(numeric_cols) > 1:
        for col in numeric_cols:
            if col != total_col:
                pct_col_name = f"{col} (%)"
                df[pct_col_name] = (df[col] / df[total_col] * 100).round(2)

        # Calculate aggregate metrics
        if "Bachelor's degree" in df.columns and "Master's degree" in df.columns:
            df["Bachelor's degree or higher"] = df[
                [
                    col
                    for col in df.columns
                    if any(
                        x in col
                        for x in ["Bachelor's", "Master's", "Professional", "Doctorate"]
                    )
                ]
            ].sum(axis=1)
            df["Bachelor's degree or higher (%)"] = (
                df["Bachelor's degree or higher"] / df[total_col] * 100
            ).round(2)

        print("✓ Calculated percentage distributions")
        print("✓ Created aggregate education categories")

    return df


def save_data(df, geography, year, state=None):
    """Save data to the data lake."""
    if df is None or df.empty:
        print("⚠ No data to save")
        return None

    # Create output directory
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    state_suffix = f"_{state}" if state else ""
    filename = f"census_education_{year}_{geography}{state_suffix}_{timestamp}.csv"
    output_file = output_dir / filename

    print(f"\nSaving data...")
    df.to_csv(output_file, index=False)

    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Records: {len(df):,}")
    print(f"✓ Size: {file_size_mb:.2f} MB")

    return output_file


def show_preview(df):
    """Show a preview of the data."""
    if df is None or df.empty:
        return

    print("\n" + "=" * 80)
    print("DATA PREVIEW (first 5 rows)")
    print("=" * 80 + "\n")

    # Show subset of columns for readability
    display_cols = [col for col in df.columns if not col.endswith("(%)")][:10]
    print(df[display_cols].head())

    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80 + "\n")

    # Show summary for key education levels
    key_cols = [
        col
        for col in df.columns
        if any(
            x in col
            for x in [
                "Bachelor's",
                "Master's",
                "High school",
                "No schooling",
                "or higher",
            ]
        )
    ]

    if key_cols:
        print(df[key_cols].describe())


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Fetch educational attainment data from US Census Bureau",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # National level education data
  python scripts/fetch_census_education.py --geography us

  # All states education data
  python scripts/fetch_census_education.py --geography state

  # California counties
  python scripts/fetch_census_education.py --geography county --state 06

  # New York state detailed breakdown
  python scripts/fetch_census_education.py --geography state --state 36 --detailed

  # Census tracts in Texas
  python scripts/fetch_census_education.py --geography tract --state 48

Common State FIPS Codes:
  06 = California    36 = New York      48 = Texas
  12 = Florida       17 = Illinois      42 = Pennsylvania
  13 = Georgia       39 = Ohio          53 = Washington

See full list: https://www.census.gov/library/reference/code-lists/ansi.html

Note: Requires free Census API key from https://api.census.gov/data/key_signup.html
      Add to .env file: CENSUS_API_KEY=your_key_here
        """,
    )

    parser.add_argument(
        "--geography",
        required=True,
        choices=["us", "state", "county", "tract"],
        help="Geographic level (us=national, state=all states, county=counties, tract=census tracts)",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2021,
        help="Year for ACS 5-Year estimates (default: 2021, most recent)",
    )
    parser.add_argument(
        "--state",
        help="State FIPS code (required for county/tract, e.g., 06 for California)",
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Use detailed education variables (25 categories instead of 14)",
    )
    parser.add_argument(
        "--preview", action="store_true", help="Show data preview after fetching"
    )
    parser.add_argument(
        "--no-metrics",
        action="store_true",
        help="Skip calculating percentage and aggregate metrics",
    )

    args = parser.parse_args()

    try:
        # Fetch data
        df = fetch_acs_education(
            geography=args.geography,
            year=args.year,
            state=args.state,
            detailed=args.detailed,
        )

        if df is None:
            sys.exit(1)

        # Calculate metrics
        if not args.no_metrics:
            df = calculate_education_metrics(df)

        # Show preview
        if args.preview:
            show_preview(df)

        # Save data
        output_file = save_data(df, args.geography, args.year, args.state)

        if output_file:
            print("\n" + "=" * 80)
            print("SUCCESS! Next Steps:")
            print("=" * 80)
            print("\n1. Load and explore in Python:")
            print(f"   import pandas as pd")
            print(f"   df = pd.read_csv('{output_file}')")
            print(f"   print(df.describe())")
            print("\n2. Open in Jupyter for analysis:")
            print(f"   jupyter lab")
            print("\n3. Create visualizations:")
            print(f"   - State-by-state education comparisons")
            print(f"   - Geographic heatmaps of education levels")
            print(f"   - Correlation with economic indicators")
            print()

    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
