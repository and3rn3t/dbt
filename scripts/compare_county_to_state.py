"""
Compare Scott County data to Iowa state averages.

Shows how Scott County performs relative to the state across education,
income, demographics, housing, and employment metrics.
"""

import glob
from pathlib import Path

import pandas as pd

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_latest_data(pattern: str) -> pd.DataFrame:
    """Load the most recent file matching the pattern."""
    files = glob.glob(str(DATA_DIR / pattern))
    if not files:
        return None
    latest_file = max(files)
    return pd.read_csv(latest_file)


def compare_education(county_df: pd.DataFrame, state_df: pd.DataFrame):
    """Compare education metrics."""
    print("\n" + "=" * 80)
    print("EDUCATION COMPARISON")
    print("=" * 80)

    # Handle different column names between county and state files
    county_bach_col = (
        "Bachelor's degree or higher (%)"
        if "Bachelor's degree or higher (%)" in county_df.columns
        else "bachelors_plus_pct"
    )
    state_bach_col = (
        "bachelors_plus_pct"
        if "bachelors_plus_pct" in state_df.columns
        else "Bachelor's degree or higher (%)"
    )

    county_bach = county_df[county_bach_col].values[0]
    state_bach = state_df[state_bach_col].values[0]
    diff = county_bach - state_bach

    print(f"\nBachelor's Degree or Higher (Age 25+):")
    print(f"  Scott County: {county_bach:.1f}%")
    print(f"  Iowa State:   {state_bach:.1f}%")
    print(f"  Difference:   {diff:+.1f} pts", end="")

    if diff > 0:
        print(f" (County is {diff:.1f} pts above state average)")
    else:
        print(f" (County is {abs(diff):.1f} pts below state average)")


def compare_income(county_df: pd.DataFrame, state_df: pd.DataFrame):
    """Compare income metrics."""
    print("\n" + "=" * 80)
    print("INCOME COMPARISON")
    print("=" * 80)

    # Handle different column names
    county_income_col = (
        "Median household income in the past 12 months (in 2021 inflation-adjusted dollars)"
        if "Median household income in the past 12 months (in 2021 inflation-adjusted dollars)"
        in county_df.columns
        else "B19013_001E"
    )
    state_income_col = "B19013_001E"

    county_income = county_df[county_income_col].values[0]
    state_income = state_df[state_income_col].values[0]
    diff = county_income - state_income
    pct_diff = diff / state_income * 100

    print("\nMedian Household Income:")
    print(f"  Scott County: ${county_income:,.0f}")
    print(f"  Iowa State:   ${state_income:,.0f}")
    print(f"  Difference:   ${diff:+,.0f} ({pct_diff:+.1f}%)")

    # Poverty rate
    county_poverty_col = (
        "Poverty rate (%)"
        if "Poverty rate (%)" in county_df.columns
        else "poverty_rate_pct"
    )
    state_poverty_col = "poverty_rate_pct"

    county_poverty = county_df[county_poverty_col].values[0]
    state_poverty = state_df[state_poverty_col].values[0]
    diff_poverty = county_poverty - state_poverty

    print("\nPoverty Rate:")
    print(f"  Scott County: {county_poverty:.1f}%")
    print(f"  Iowa State:   {state_poverty:.1f}%")
    print(f"  Difference:   {diff_poverty:+.1f} pts")


def compare_demographics(county_df: pd.DataFrame, state_df: pd.DataFrame):
    """Compare demographic metrics."""
    print("\n" + "=" * 80)
    print("DEMOGRAPHICS COMPARISON")
    print("=" * 80)

    county_pop = county_df["B01003_001E"].values[0]
    state_pop = state_df["B01003_001E"].values[0]

    print(f"\nTotal Population:")
    print(f"  Scott County: {county_pop:,.0f}")
    print(f"  Iowa State:   {state_pop:,.0f}")
    print(f"  County is {(county_pop/state_pop*100):.1f}% of state population")

    county_age = county_df["B01002_001E"].values[0]
    state_age = state_df["B01002_001E"].values[0]

    print(f"\nMedian Age:")
    print(f"  Scott County: {county_age:.1f} years")
    print(f"  Iowa State:   {state_age:.1f} years")
    print(f"  Difference:   {(county_age - state_age):+.1f} years")


def compare_housing(county_df: pd.DataFrame, state_df: pd.DataFrame):
    """Compare housing metrics."""
    print("\n" + "=" * 80)
    print("HOUSING COMPARISON")
    print("=" * 80)

    county_value = county_df["B25077_001E"].values[0]
    state_value = state_df["B25077_001E"].values[0]
    diff = county_value - state_value
    pct_diff = diff / state_value * 100

    print(f"\nMedian Home Value:")
    print(f"  Scott County: ${county_value:,.0f}")
    print(f"  Iowa State:   ${state_value:,.0f}")
    print(f"  Difference:   ${diff:+,.0f} ({pct_diff:+.1f}%)")

    county_rent = county_df["B25064_001E"].values[0]
    state_rent = state_df["B25064_001E"].values[0]

    print(f"\nMedian Gross Rent:")
    print(f"  Scott County: ${county_rent:,.0f}/month")
    print(f"  Iowa State:   ${state_rent:,.0f}/month")
    print(f"  Difference:   ${(county_rent - state_rent):+,.0f}/month")

    county_owner = county_df["owner_occupied_pct"].values[0]
    state_owner = state_df["owner_occupied_pct"].values[0]

    print(f"\nHomeownership Rate:")
    print(f"  Scott County: {county_owner:.1f}%")
    print(f"  Iowa State:   {state_owner:.1f}%")
    print(f"  Difference:   {(county_owner - state_owner):+.1f} pts")


def compare_employment(county_df: pd.DataFrame, state_df: pd.DataFrame):
    """Compare employment metrics."""
    print("\n" + "=" * 80)
    print("EMPLOYMENT COMPARISON")
    print("=" * 80)

    county_lfp = county_df["labor_force_participation_pct"].values[0]
    state_lfp = state_df["labor_force_participation_pct"].values[0]

    print(f"\nLabor Force Participation Rate:")
    print(f"  Scott County: {county_lfp:.1f}%")
    print(f"  Iowa State:   {state_lfp:.1f}%")
    print(f"  Difference:   {(county_lfp - state_lfp):+.1f} pts")

    county_unemp = county_df["unemployment_rate_pct"].values[0]
    state_unemp = state_df["unemployment_rate_pct"].values[0]

    print(f"\nUnemployment Rate:")
    print(f"  Scott County: {county_unemp:.1f}%")
    print(f"  Iowa State:   {state_unemp:.1f}%")
    print(f"  Difference:   {(county_unemp - state_unemp):+.1f} pts")


def main():
    """Main comparison function."""
    print("\n" + "=" * 80)
    print("SCOTT COUNTY vs IOWA STATE COMPARISON")
    print("=" * 80)

    # Load data
    datasets = ["education", "income", "demographics", "housing", "employment"]

    for dataset in datasets:
        county_df = load_latest_data(f"scott_county_iowa_{dataset}_2021_*.csv")
        state_df = load_latest_data(f"iowa_state_{dataset}_2021_*.csv")

        if county_df is None:
            print(f"\nWarning: No Scott County {dataset} data found")
            continue
        if state_df is None:
            print(f"\nWarning: No Iowa state {dataset} data found")
            print(f"Run: python scripts/fetch_iowa_state_data.py")
            continue

        # Compare
        if dataset == "education":
            compare_education(county_df, state_df)
        elif dataset == "income":
            compare_income(county_df, state_df)
        elif dataset == "demographics":
            compare_demographics(county_df, state_df)
        elif dataset == "housing":
            compare_housing(county_df, state_df)
        elif dataset == "employment":
            compare_employment(county_df, state_df)

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
    main()
    main()
    main()
    main()
