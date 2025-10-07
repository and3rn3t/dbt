"""
Analyze year-over-year changes in Scott County and Iowa state data.

Shows annual changes and growth rates for key metrics.
"""

import glob
from pathlib import Path

import pandas as pd

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_historical_data(pattern: str) -> pd.DataFrame:
    """Load the most recent historical file matching the pattern."""
    files = glob.glob(str(DATA_DIR / pattern))
    if not files:
        return None
    latest_file = max(files)
    return pd.read_csv(latest_file)


def analyze_education_yoy(df: pd.DataFrame, location_name: str):
    """Analyze year-over-year education changes."""
    print(f"\n{'='*80}")
    print(f"{location_name} - EDUCATION YEAR-OVER-YEAR CHANGES")
    print(f"{'='*80}")

    df = df.sort_values("year").copy()
    df["bach_plus_yoy"] = df["bachelors_plus_pct"].diff()

    print(f"\n{'Year':<8} {'Bach+%':<10} {'YoY Change':<12} {'Notes'}")
    print("-" * 80)

    for _, row in df.iterrows():
        year = int(row["year"])
        bach = row["bachelors_plus_pct"]
        yoy = row["bach_plus_yoy"]

        note = ""
        if pd.notna(yoy):
            if yoy > 1.0:
                note = "Strong growth"
            elif yoy < 0:
                note = "Decline"

        yoy_str = f"{yoy:+.2f} pts" if pd.notna(yoy) else "-"
        print(f"{year:<8} {bach:>7.1f}%   {yoy_str:<12} {note}")

    # Summary statistics
    avg_yoy = df["bach_plus_yoy"].mean()
    print(f"\nAverage YoY Change: {avg_yoy:+.2f} percentage points/year")


def analyze_income_yoy(df: pd.DataFrame, location_name: str):
    """Analyze year-over-year income changes."""
    print(f"\n{'='*80}")
    print(f"{location_name} - INCOME YEAR-OVER-YEAR CHANGES")
    print(f"{'='*80}")

    df = df.sort_values("year").copy()
    df["income_yoy"] = df["B19013_001E"].diff()
    df["income_pct_change"] = df["income_yoy"] / df["B19013_001E"].shift(1) * 100

    print(f"\n{'Year':<8} {'Income':<12} {'YoY $':<12} {'YoY %':<10} {'Notes'}")
    print("-" * 80)

    for _, row in df.iterrows():
        year = int(row["year"])
        income = row["B19013_001E"]
        yoy_dollars = row["income_yoy"]
        yoy_pct = row["income_pct_change"]

        note = ""
        if pd.notna(yoy_pct):
            if yoy_pct > 5:
                note = "Strong growth"
            elif yoy_pct < 0:
                note = "Decline"
            elif yoy_pct < 2:
                note = "Below inflation"

        yoy_d_str = f"${yoy_dollars:+,.0f}" if pd.notna(yoy_dollars) else "-"
        yoy_p_str = f"{yoy_pct:+.1f}%" if pd.notna(yoy_pct) else "-"

        print(f"{year:<8} ${income:>10,.0f} {yoy_d_str:<12} {yoy_p_str:<10} {note}")

    # Summary statistics
    avg_yoy_pct = df["income_pct_change"].mean()
    print(f"\nAverage YoY Growth: {avg_yoy_pct:+.1f}%/year")


def analyze_population_yoy(df: pd.DataFrame, location_name: str):
    """Analyze year-over-year population changes."""
    print(f"\n{'='*80}")
    print(f"{location_name} - POPULATION YEAR-OVER-YEAR CHANGES")
    print(f"{'='*80}")

    df = df.sort_values("year").copy()
    df["pop_yoy"] = df["B01003_001E"].diff()
    df["pop_pct_change"] = df["pop_yoy"] / df["B01003_001E"].shift(1) * 100

    print(
        f"\n{'Year':<8} {'Population':<14} {'YoY Change':<14} {'YoY %':<10} {'Notes'}"
    )
    print("-" * 80)

    for _, row in df.iterrows():
        year = int(row["year"])
        pop = row["B01003_001E"]
        yoy = row["pop_yoy"]
        yoy_pct = row["pop_pct_change"]

        note = ""
        if pd.notna(yoy_pct):
            if yoy_pct > 1:
                note = "Rapid growth"
            elif yoy_pct < 0:
                note = "Population loss"

        yoy_str = f"{yoy:+,.0f}" if pd.notna(yoy) else "-"
        yoy_p_str = f"{yoy_pct:+.2f}%" if pd.notna(yoy_pct) else "-"

        print(f"{year:<8} {pop:>12,.0f}  {yoy_str:<14} {yoy_p_str:<10} {note}")

    # Summary statistics
    avg_yoy = df["pop_yoy"].mean()
    avg_yoy_pct = df["pop_pct_change"].mean()
    print(f"\nAverage YoY Change: {avg_yoy:+,.0f} people/year ({avg_yoy_pct:+.2f}%)")


def analyze_housing_yoy(df: pd.DataFrame, location_name: str):
    """Analyze year-over-year housing changes."""
    print(f"\n{'='*80}")
    print(f"{location_name} - HOUSING YEAR-OVER-YEAR CHANGES")
    print(f"{'='*80}")

    df = df.sort_values("year").copy()
    df["value_yoy"] = df["B25077_001E"].diff()
    df["value_pct_change"] = df["value_yoy"] / df["B25077_001E"].shift(1) * 100

    print(f"\n{'Year':<8} {'Home Value':<14} {'YoY $':<14} {'YoY %':<10} {'Notes'}")
    print("-" * 80)

    for _, row in df.iterrows():
        year = int(row["year"])
        value = row["B25077_001E"]
        yoy = row["value_yoy"]
        yoy_pct = row["value_pct_change"]

        note = ""
        if pd.notna(yoy_pct):
            if yoy_pct > 5:
                note = "Strong appreciation"
            elif yoy_pct < 0:
                note = "Depreciation"

        yoy_str = f"${yoy:+,.0f}" if pd.notna(yoy) else "-"
        yoy_p_str = f"{yoy_pct:+.1f}%" if pd.notna(yoy_pct) else "-"

        print(f"{year:<8} ${value:>11,.0f}  {yoy_str:<14} {yoy_p_str:<10} {note}")

    # Summary statistics
    avg_yoy_pct = df["value_pct_change"].mean()
    print(f"\nAverage YoY Appreciation: {avg_yoy_pct:+.1f}%/year")


def main():
    """Main analysis function."""
    print("\n" + "=" * 80)
    print("YEAR-OVER-YEAR CHANGE ANALYSIS")
    print("=" * 80)

    # Analyze Scott County
    print("\n" + "=" * 80)
    print("SCOTT COUNTY, IOWA")
    print("=" * 80)

    county_education = load_historical_data(
        "scott_county_iowa_education_historical_*.csv"
    )
    if county_education is not None:
        analyze_education_yoy(county_education, "Scott County")

    county_income = load_historical_data("scott_county_iowa_income_historical_*.csv")
    if county_income is not None:
        analyze_income_yoy(county_income, "Scott County")

    county_demographics = load_historical_data(
        "scott_county_iowa_demographics_historical_*.csv"
    )
    if county_demographics is not None:
        analyze_population_yoy(county_demographics, "Scott County")

    county_housing = load_historical_data("scott_county_iowa_housing_historical_*.csv")
    if county_housing is not None:
        analyze_housing_yoy(county_housing, "Scott County")

    # Analyze Iowa State (if available)
    state_education = load_historical_data("iowa_state_education_historical_*.csv")
    if state_education is not None:
        print("\n\n" + "=" * 80)
        print("IOWA STATE")
        print("=" * 80)

        analyze_education_yoy(state_education, "Iowa State")

        state_income = load_historical_data("iowa_state_income_historical_*.csv")
        if state_income is not None:
            analyze_income_yoy(state_income, "Iowa State")

        state_demographics = load_historical_data(
            "iowa_state_demographics_historical_*.csv"
        )
        if state_demographics is not None:
            analyze_population_yoy(state_demographics, "Iowa State")

        state_housing = load_historical_data("iowa_state_housing_historical_*.csv")
        if state_housing is not None:
            analyze_housing_yoy(state_housing, "Iowa State")
    else:
        print("\n\nNote: Iowa state historical data not available.")
        print("Run: python scripts/fetch_iowa_state_data.py historical")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
    main()
    main()
    main()
    main()
