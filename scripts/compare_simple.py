"""
Simple comparison script that works with actual column names.
"""

import glob
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_latest(pattern):
    """Load most recent file matching pattern."""
    files = glob.glob(str(DATA_DIR / pattern))
    if not files:
        return None
    return pd.read_csv(max(files))


def main():
    print("\n" + "=" * 80)
    print("SCOTT COUNTY vs IOWA STATE - 2021 COMPARISON")
    print("=" * 80)

    # Load data
    county_edu = load_latest("scott_county_iowa_education_2021_*.csv")
    state_edu = load_latest("iowa_state_education_2021_*.csv")

    county_inc = load_latest("scott_county_iowa_income_2021_*.csv")
    state_inc = load_latest("iowa_state_income_2021_*.csv")

    county_dem = load_latest("scott_county_iowa_demographics_2021_*.csv")
    state_dem = load_latest("iowa_state_demographics_2021_*.csv")

    county_hou = load_latest("scott_county_iowa_housing_2021_*.csv")
    state_hou = load_latest("iowa_state_housing_2021_*.csv")

    county_emp = load_latest("scott_county_iowa_employment_2021_*.csv")
    state_emp = load_latest("iowa_state_employment_2021_*.csv")

    # Education
    if county_edu is not None and state_edu is not None:
        print("\n" + "=" * 80)
        print("EDUCATION")
        print("=" * 80)

        county_bach = county_edu["Bachelor's degree or higher (%)"].values[0]
        state_bach = state_edu["bachelors_plus_pct"].values[0]

        print(f"\nBachelor's Degree or Higher (Age 25+):")
        print(f"  Scott County: {county_bach:.1f}%")
        print(f"  Iowa State:   {state_bach:.1f}%")
        print(f"  Difference:   {(county_bach - state_bach):+.1f} pts")

        if county_bach > state_bach:
            print(
                f"  → Scott County is {(county_bach - state_bach):.1f} pts ABOVE state average"
            )
        else:
            print(
                f"  → Scott County is {(state_bach - county_bach):.1f} pts BELOW state average"
            )

    # Income
    if county_inc is not None and state_inc is not None:
        print("\n" + "=" * 80)
        print("INCOME")
        print("=" * 80)

        county_income = county_inc["Median household income"].values[0]
        state_income = state_inc["B19013_001E"].values[0]

        print(f"\nMedian Household Income:")
        print(f"  Scott County: ${county_income:,.0f}")
        print(f"  Iowa State:   ${state_income:,.0f}")
        print(
            f"  Difference:   ${(county_income - state_income):+,.0f} ({((county_income - state_income) / state_income * 100):+.1f}%)"
        )

        county_poverty = county_inc["Poverty rate (%)"].values[0]
        state_poverty = state_inc["poverty_rate_pct"].values[0]

        print(f"\nPoverty Rate:")
        print(f"  Scott County: {county_poverty:.1f}%")
        print(f"  Iowa State:   {state_poverty:.1f}%")
        print(f"  Difference:   {(county_poverty - state_poverty):+.1f} pts")

    # Demographics
    if county_dem is not None and state_dem is not None:
        print("\n" + "=" * 80)
        print("DEMOGRAPHICS")
        print("=" * 80)

        county_pop = county_dem["Total population"].values[0]
        state_pop = state_dem["B01003_001E"].values[0]

        print(f"\nTotal Population:")
        print(f"  Scott County: {county_pop:,.0f}")
        print(f"  Iowa State:   {state_pop:,.0f}")
        print(f"  County is {(county_pop / state_pop * 100):.1f}% of state")

        county_age = county_dem["Median age"].values[0]
        state_age = state_dem["B01002_001E"].values[0]

        print(f"\nMedian Age:")
        print(f"  Scott County: {county_age:.1f} years")
        print(f"  Iowa State:   {state_age:.1f} years")
        print(f"  Difference:   {(county_age - state_age):+.1f} years")

    # Housing
    if county_hou is not None and state_hou is not None:
        print("\n" + "=" * 80)
        print("HOUSING")
        print("=" * 80)

        county_value = county_hou["Median value (owner-occupied units)"].values[0]
        state_value = state_hou["B25077_001E"].values[0]

        print(f"\nMedian Home Value:")
        print(f"  Scott County: ${county_value:,.0f}")
        print(f"  Iowa State:   ${state_value:,.0f}")
        print(
            f"  Difference:   ${(county_value - state_value):+,.0f} ({((county_value - state_value) / state_value * 100):+.1f}%)"
        )

        county_rent = county_hou["Median gross rent"].values[0]
        state_rent = state_hou["B25064_001E"].values[0]

        print(f"\nMedian Gross Rent:")
        print(f"  Scott County: ${county_rent:,.0f}/month")
        print(f"  Iowa State:   ${state_rent:,.0f}/month")
        print(f"  Difference:   ${(county_rent - state_rent):+,.0f}/month")

        county_owner = county_hou["Owner occupied (%)"].values[0]
        state_owner = state_hou["owner_occupied_pct"].values[0]

        print(f"\nHomeownership Rate:")
        print(f"  Scott County: {county_owner:.1f}%")
        print(f"  Iowa State:   {state_owner:.1f}%")
        print(f"  Difference:   {(county_owner - state_owner):+.1f} pts")

    # Employment
    if county_emp is not None and state_emp is not None:
        print("\n" + "=" * 80)
        print("EMPLOYMENT")
        print("=" * 80)

        county_lfp = county_emp["Labor force participation rate (%)"].values[0]
        state_lfp = state_emp["labor_force_participation_pct"].values[0]

        print(f"\nLabor Force Participation Rate:")
        print(f"  Scott County: {county_lfp:.1f}%")
        print(f"  Iowa State:   {state_lfp:.1f}%")
        print(f"  Difference:   {(county_lfp - state_lfp):+.1f} pts")

        county_unemp = county_emp["Unemployment rate (%)"].values[0]
        state_unemp = state_emp["unemployment_rate_pct"].values[0]

        print(f"\nUnemployment Rate:")
        print(f"  Scott County: {county_unemp:.1f}%")
        print(f"  Iowa State:   {state_unemp:.1f}%")
        print(f"  Difference:   {(county_unemp - state_unemp):+.1f} pts")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
    main()
    main()
    main()
    main()
