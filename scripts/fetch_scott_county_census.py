#!/usr/bin/env python3
"""
Fetch comprehensive Census data for Scott County, Iowa.

This script pulls multiple datasets from the Census Bureau API:
- Educational Attainment
- Income and Poverty
- Demographics (Age, Race, Ethnicity)
- Housing Characteristics
- Employment and Industry

Scott County, Iowa:
- State FIPS: 19 (Iowa)
- County FIPS: 163 (Scott County)
- Major cities: Davenport, Bettendorf

Usage:
    python scripts/fetch_scott_county_census.py
    python scripts/fetch_scott_county_census.py --year 2021
    python scripts/fetch_scott_county_census.py --detailed
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

# Scott County, Iowa identifiers
STATE_FIPS = "19"  # Iowa
COUNTY_FIPS = "163"  # Scott County
LOCATION_NAME = "Scott County, Iowa"

# Census Variable Groups for Comprehensive Data
CENSUS_DATASETS = {
    "education": {
        "name": "Educational Attainment",
        "variables": {
            "B15003_001E": "Total population 25 years and over",
            "B15003_017E": "High school graduate (includes equivalency)",
            "B15003_018E": "Some college, less than 1 year",
            "B15003_019E": "Some college, 1 or more years, no degree",
            "B15003_020E": "Associate's degree",
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
            "B19025_001E": "Aggregate household income",
            "B19301_001E": "Per capita income",
            "B17001_001E": "Population for whom poverty status is determined",
            "B17001_002E": "Income in the past 12 months below poverty level",
            "B19001_001E": "Total households (income)",
            "B19001_002E": "Households with income less than $10,000",
            "B19001_003E": "Households with income $10,000 to $14,999",
            "B19001_004E": "Households with income $15,000 to $19,999",
            "B19001_005E": "Households with income $20,000 to $24,999",
            "B19001_006E": "Households with income $25,000 to $29,999",
            "B19001_007E": "Households with income $30,000 to $34,999",
            "B19001_008E": "Households with income $35,000 to $39,999",
            "B19001_009E": "Households with income $40,000 to $44,999",
            "B19001_010E": "Households with income $45,000 to $49,999",
            "B19001_011E": "Households with income $50,000 to $59,999",
            "B19001_012E": "Households with income $60,000 to $74,999",
            "B19001_013E": "Households with income $75,000 to $99,999",
            "B19001_014E": "Households with income $100,000 to $124,999",
            "B19001_015E": "Households with income $125,000 to $149,999",
            "B19001_016E": "Households with income $150,000 to $199,999",
            "B19001_017E": "Households with income $200,000 or more",
        },
    },
    "demographics": {
        "name": "Age, Race, and Ethnicity",
        "variables": {
            "B01001_001E": "Total population",
            "B01002_001E": "Median age",
            "B01001_003E": "Male: Under 5 years",
            "B01001_004E": "Male: 5 to 9 years",
            "B01001_005E": "Male: 10 to 14 years",
            "B01001_006E": "Male: 15 to 17 years",
            "B01001_007E": "Male: 18 and 19 years",
            "B01001_008E": "Male: 20 years",
            "B01001_009E": "Male: 21 years",
            "B01001_010E": "Male: 22 to 24 years",
            "B01001_011E": "Male: 25 to 29 years",
            "B01001_012E": "Male: 30 to 34 years",
            "B01001_013E": "Male: 35 to 39 years",
            "B01001_014E": "Male: 40 to 44 years",
            "B01001_015E": "Male: 45 to 49 years",
            "B01001_016E": "Male: 50 to 54 years",
            "B01001_017E": "Male: 55 to 59 years",
            "B01001_018E": "Male: 60 and 61 years",
            "B01001_019E": "Male: 62 to 64 years",
            "B01001_020E": "Male: 65 and 66 years",
            "B01001_021E": "Male: 67 to 69 years",
            "B01001_022E": "Male: 70 to 74 years",
            "B01001_023E": "Male: 75 to 79 years",
            "B01001_024E": "Male: 80 to 84 years",
            "B01001_025E": "Male: 85 years and over",
            "B02001_001E": "Total population (race)",
            "B02001_002E": "White alone",
            "B02001_003E": "Black or African American alone",
            "B02001_004E": "American Indian and Alaska Native alone",
            "B02001_005E": "Asian alone",
            "B02001_006E": "Native Hawaiian and Other Pacific Islander alone",
            "B02001_007E": "Some other race alone",
            "B02001_008E": "Two or more races",
            "B03001_001E": "Total population (Hispanic origin)",
            "B03001_003E": "Hispanic or Latino",
        },
    },
    "housing": {
        "name": "Housing Characteristics",
        "variables": {
            "B25001_001E": "Total housing units",
            "B25002_001E": "Total housing units (occupancy)",
            "B25002_002E": "Occupied housing units",
            "B25002_003E": "Vacant housing units",
            "B25003_001E": "Total occupied housing units",
            "B25003_002E": "Owner occupied",
            "B25003_003E": "Renter occupied",
            "B25077_001E": "Median value (owner-occupied units)",
            "B25064_001E": "Median gross rent",
            "B25024_001E": "Total housing units (units in structure)",
            "B25024_002E": "1, detached",
            "B25024_003E": "1, attached",
            "B25024_004E": "2 units",
            "B25024_005E": "3 or 4 units",
            "B25024_006E": "5 to 9 units",
            "B25024_007E": "10 to 19 units",
            "B25024_008E": "20 to 49 units",
            "B25024_009E": "50 or more units",
            "B25024_010E": "Mobile home",
        },
    },
    "employment": {
        "name": "Employment and Industry",
        "variables": {
            "B23025_001E": "Population 16 years and over",
            "B23025_002E": "In labor force",
            "B23025_003E": "Civilian labor force",
            "B23025_004E": "Employed",
            "B23025_005E": "Unemployed",
            "B23025_006E": "Armed Forces",
            "B23025_007E": "Not in labor force",
            "C24030_001E": "Total employed (by industry)",
            "C24030_003E": "Agriculture, forestry, fishing and hunting, and mining",
            "C24030_006E": "Construction",
            "C24030_009E": "Manufacturing",
            "C24030_012E": "Wholesale trade",
            "C24030_015E": "Retail trade",
            "C24030_018E": "Transportation and warehousing, and utilities",
            "C24030_021E": "Information",
            "C24030_024E": "Finance and insurance, and real estate",
            "C24030_027E": "Professional, scientific, management, administrative",
            "C24030_030E": "Educational services, health care, social assistance",
            "C24030_033E": "Arts, entertainment, recreation, accommodation, food",
            "C24030_036E": "Other services, except public administration",
            "C24030_039E": "Public administration",
        },
    },
}


def check_api_key():
    """Check if Census API key is available."""
    api_key = os.getenv("CENSUS_API_KEY")

    if not api_key:
        print("\nℹ️  No Census API key found (optional - will work without it)")
        print("   Get one at: https://api.census.gov/data/key_signup.html")
        print("   for higher rate limits\n")
        return None

    # Validate key format (Census keys are typically 40 chars)
    if len(api_key) < 30:
        print("\n⚠️  Census API key looks invalid (too short)")
        print("   Proceeding without key...\n")
        return None

    return api_key


def fetch_dataset(dataset_name, dataset_info, year=2021):
    """Fetch a specific dataset for Scott County."""
    api_key = check_api_key()

    variables = dataset_info["variables"]
    var_list = ",".join(variables.keys())

    base_url = f"https://api.census.gov/data/{year}/acs/acs5"

    print(f"\n{'='*80}")
    print(f"Fetching: {dataset_info['name']}")
    print(f"{'='*80}")
    print(f"Location: {LOCATION_NAME}")
    print(f"Variables: {len(variables)}")
    print(f"Year: {year} ACS 5-Year Estimates")

    params = {
        "get": f"NAME,{var_list}",
        "for": f"county:{COUNTY_FIPS}",
        "in": f"state:{STATE_FIPS}",
    }

    # Add key only if available
    if api_key:
        params["key"] = api_key

    try:
        print("Downloading...")
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Rename columns
        for var_code, var_name in variables.items():
            if var_code in df.columns:
                df.rename(columns={var_code: var_name}, inplace=True)

        # Convert numeric columns
        for col in df.columns:
            if col not in ["NAME", "state", "county"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        print(f"✓ Downloaded {len(df.columns) - 3} indicators")

        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        if hasattr(e, "response") and hasattr(e.response, "text"):
            print(f"   Response: {e.response.text[:200]}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def calculate_metrics(df, dataset_name):
    """Calculate percentages and derived metrics."""

    # Education metrics
    if dataset_name == "education":
        total_col = "Total population 25 years and over"
        if total_col in df.columns:
            # Calculate bachelor's or higher
            bachelor_cols = [
                "Bachelor's degree",
                "Master's degree",
                "Professional school degree",
                "Doctorate degree",
            ]
            available_cols = [col for col in bachelor_cols if col in df.columns]
            if available_cols:
                df["Bachelor's degree or higher"] = df[available_cols].sum(axis=1)
                df["Bachelor's degree or higher (%)"] = (
                    df["Bachelor's degree or higher"] / df[total_col] * 100
                ).round(2)

            # Calculate percentages for all education levels
            for col in df.columns:
                if col not in [
                    total_col,
                    "NAME",
                    "state",
                    "county",
                ] and not col.endswith("(%)"):
                    df[f"{col} (%)"] = (df[col] / df[total_col] * 100).round(2)

    # Income metrics
    elif dataset_name == "income":
        if "Population for whom poverty status is determined" in df.columns:
            poverty_col = "Income in the past 12 months below poverty level"
            if poverty_col in df.columns:
                df["Poverty rate (%)"] = (
                    df[poverty_col]
                    / df["Population for whom poverty status is determined"]
                    * 100
                ).round(2)

    # Demographics metrics
    elif dataset_name == "demographics":
        if "Total population" in df.columns:
            total = df["Total population"].iloc[0]

            # Race percentages
            race_cols = [
                "White alone",
                "Black or African American alone",
                "American Indian and Alaska Native alone",
                "Asian alone",
                "Native Hawaiian and Other Pacific Islander alone",
                "Some other race alone",
                "Two or more races",
            ]
            for col in race_cols:
                if col in df.columns:
                    df[f"{col} (%)"] = (df[col] / total * 100).round(2)

            # Hispanic/Latino percentage
            if "Hispanic or Latino" in df.columns:
                df["Hispanic or Latino (%)"] = (
                    df["Hispanic or Latino"]
                    / df["Total population (Hispanic origin)"]
                    * 100
                ).round(2)

    # Housing metrics
    elif dataset_name == "housing":
        if "Total occupied housing units" in df.columns:
            total = df["Total occupied housing units"].iloc[0]
            if "Owner occupied" in df.columns:
                df["Owner occupied (%)"] = (df["Owner occupied"] / total * 100).round(2)
            if "Renter occupied" in df.columns:
                df["Renter occupied (%)"] = (df["Renter occupied"] / total * 100).round(
                    2
                )

        if "Total housing units (occupancy)" in df.columns:
            total = df["Total housing units (occupancy)"].iloc[0]
            if "Vacant housing units" in df.columns:
                df["Vacancy rate (%)"] = (
                    df["Vacant housing units"] / total * 100
                ).round(2)

    # Employment metrics
    elif dataset_name == "employment":
        if "Civilian labor force" in df.columns and "Unemployed" in df.columns:
            df["Unemployment rate (%)"] = (
                df["Unemployed"] / df["Civilian labor force"] * 100
            ).round(2)

        if (
            "Population 16 years and over" in df.columns
            and "In labor force" in df.columns
        ):
            df["Labor force participation rate (%)"] = (
                df["In labor force"] / df["Population 16 years and over"] * 100
            ).round(2)

    return df


def save_dataset(df, dataset_name, year):
    """Save dataset to file."""
    if df is None or df.empty:
        return None

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scott_county_iowa_{dataset_name}_{year}_{timestamp}.csv"
    output_file = output_dir / filename

    df.to_csv(output_file, index=False)

    file_size_kb = output_file.stat().st_size / 1024
    print(f"✓ Saved: {output_file.name}")
    print(f"✓ Size: {file_size_kb:.2f} KB")

    return output_file


def create_summary_report(all_data, year):
    """Create a comprehensive summary report."""
    print("\n" + "=" * 80)
    print(f"SCOTT COUNTY, IOWA - CENSUS DATA SUMMARY ({year})")
    print("=" * 80)

    for dataset_name, df in all_data.items():
        if df is None or df.empty:
            continue

        print(f"\n📊 {CENSUS_DATASETS[dataset_name]['name']}")
        print("-" * 80)

        if dataset_name == "education":
            bach_col = "Bachelor's degree or higher (%)"
            if bach_col in df.columns:
                print(f"   College educated (bachelor's+): {df[bach_col].iloc[0]:.1f}%")
            if "High school graduate (includes equivalency)" in df.columns:
                print(
                    f"   High school graduates: {df['High school graduate (includes equivalency)'].iloc[0]:,.0f}"
                )

        elif dataset_name == "income":
            if "Median household income" in df.columns:
                print(
                    f"   Median household income: ${df['Median household income'].iloc[0]:,.0f}"
                )
            if "Per capita income" in df.columns:
                print(f"   Per capita income: ${df['Per capita income'].iloc[0]:,.0f}")
            if "Poverty rate (%)" in df.columns:
                print(f"   Poverty rate: {df['Poverty rate (%)'].iloc[0]:.1f}%")

        elif dataset_name == "demographics":
            if "Total population" in df.columns:
                print(f"   Total population: {df['Total population'].iloc[0]:,.0f}")
            if "Median age" in df.columns:
                print(f"   Median age: {df['Median age'].iloc[0]:.1f} years")
            if "White alone (%)" in df.columns:
                print(f"   White: {df['White alone (%)'].iloc[0]:.1f}%")
            if "Hispanic or Latino (%)" in df.columns:
                print(
                    f"   Hispanic or Latino: {df['Hispanic or Latino (%)'].iloc[0]:.1f}%"
                )

        elif dataset_name == "housing":
            if "Total housing units" in df.columns:
                print(
                    f"   Total housing units: {df['Total housing units'].iloc[0]:,.0f}"
                )
            if "Owner occupied (%)" in df.columns:
                print(f"   Homeownership rate: {df['Owner occupied (%)'].iloc[0]:.1f}%")
            if "Median value (owner-occupied units)" in df.columns:
                print(
                    f"   Median home value: ${df['Median value (owner-occupied units)'].iloc[0]:,.0f}"
                )
            if "Median gross rent" in df.columns:
                print(f"   Median rent: ${df['Median gross rent'].iloc[0]:,.0f}")

        elif dataset_name == "employment":
            if "Unemployment rate (%)" in df.columns:
                print(
                    f"   Unemployment rate: {df['Unemployment rate (%)'].iloc[0]:.1f}%"
                )
            if "Labor force participation rate (%)" in df.columns:
                print(
                    f"   Labor force participation: {df['Labor force participation rate (%)'].iloc[0]:.1f}%"
                )
            if "Employed" in df.columns:
                print(f"   Total employed: {df['Employed'].iloc[0]:,.0f}")

    print("\n" + "=" * 80)


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Fetch comprehensive Census data for Scott County, Iowa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script fetches multiple Census datasets for Scott County, Iowa:
  - Educational Attainment
  - Income and Poverty
  - Demographics (Age, Race, Ethnicity)
  - Housing Characteristics
  - Employment and Industry

All data is saved to data/raw/ directory.

Requires: Free Census API key from https://api.census.gov/data/key_signup.html
          Add to .env file: CENSUS_API_KEY=your_key_here
        """,
    )

    parser.add_argument(
        "--year",
        type=int,
        default=2021,
        help="Year for ACS 5-Year estimates (default: 2021)",
    )
    parser.add_argument(
        "--dataset",
        choices=list(CENSUS_DATASETS.keys()) + ["all"],
        default="all",
        help="Specific dataset to fetch (default: all)",
    )

    args = parser.parse_args()

    try:
        print("\n" + "=" * 80)
        print(f"FETCHING CENSUS DATA FOR {LOCATION_NAME}")
        print("=" * 80)
        print(f"State FIPS: {STATE_FIPS} (Iowa)")
        print(f"County FIPS: {COUNTY_FIPS} (Scott County)")
        print(f"Year: {args.year} ACS 5-Year Estimates")
        print("=" * 80)

        all_data = {}
        datasets_to_fetch = (
            CENSUS_DATASETS.keys() if args.dataset == "all" else [args.dataset]
        )

        for dataset_name in datasets_to_fetch:
            dataset_info = CENSUS_DATASETS[dataset_name]

            # Fetch data
            df = fetch_dataset(dataset_name, dataset_info, args.year)

            if df is not None:
                # Calculate metrics
                df = calculate_metrics(df, dataset_name)

                # Save data
                save_dataset(df, dataset_name, args.year)

                all_data[dataset_name] = df

        # Create summary report
        if all_data:
            create_summary_report(all_data, args.year)

            print("\n✅ SUCCESS! All Census data for Scott County, Iowa downloaded.")
            print(
                f"\n📁 Files saved to: data/raw/scott_county_iowa_*_{args.year}_*.csv"
            )
            print("\n🎯 Next Steps:")
            print(
                "   1. Load in Python: pd.read_csv('data/raw/scott_county_iowa_*.csv')"
            )
            print("   2. Open in Jupyter: jupyter lab")
            print("   3. Analyze and visualize the data")
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
