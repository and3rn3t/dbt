"""
Simple year-over-year analysis for Scott County historical data.
"""

import glob
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_historical(pattern):
    """Load most recent historical file."""
    files = glob.glob(str(DATA_DIR / pattern))
    if not files:
        return None
    return pd.read_csv(max(files))


def main():
    print("\n" + "=" * 80)
    print("SCOTT COUNTY - YEAR-OVER-YEAR CHANGES")
    print("=" * 80)

    # Education
    edu = load_historical("scott_county_iowa_education_historical_*.csv")
    if edu is not None:
        print("\n" + "=" * 80)
        print("EDUCATION")
        print("=" * 80)

        edu = edu.sort_values("year").copy()
        edu["yoy"] = edu["Bachelor's degree or higher (%)"].diff()

        print(f"\n{'Year':<8} {'Bach+%':<10} {'YoY Change':<14} {'Notes'}")
        print("-" * 80)

        for _, row in edu.iterrows():
            year = int(row["year"])
            bach = row["Bachelor's degree or higher (%)"]
            yoy = row["yoy"]

            note = ""
            if pd.notna(yoy):
                if yoy > 1.0:
                    note = "Strong growth"
                elif yoy < 0:
                    note = "Decline"

            yoy_str = f"{yoy:+.2f} pts" if pd.notna(yoy) else "-"
            print(f"{year:<8} {bach:>7.1f}%   {yoy_str:<14} {note}")

        avg_yoy = edu["yoy"].mean()
        print(f"\nAverage YoY Change: {avg_yoy:+.2f} percentage points/year")

    # Income
    inc = load_historical("scott_county_iowa_income_historical_*.csv")
    if inc is not None:
        print("\n" + "=" * 80)
        print("INCOME")
        print("=" * 80)

        inc = inc.sort_values("year").copy()
        inc["yoy_dollars"] = inc["Median household income"].diff()
        inc["yoy_pct"] = (
            inc["yoy_dollars"] / inc["Median household income"].shift(1) * 100
        )

        print(f"\n{'Year':<8} {'Income':<14} {'YoY $':<14} {'YoY %':<10} {'Notes'}")
        print("-" * 80)

        for _, row in inc.iterrows():
            year = int(row["year"])
            income = row["Median household income"]
            yoy_d = row["yoy_dollars"]
            yoy_p = row["yoy_pct"]

            note = ""
            if pd.notna(yoy_p):
                if yoy_p > 5:
                    note = "Strong growth"
                elif yoy_p < 0:
                    note = "Decline"
                elif yoy_p < 2:
                    note = "Below inflation"

            yoy_d_str = f"${yoy_d:+,.0f}" if pd.notna(yoy_d) else "-"
            yoy_p_str = f"{yoy_p:+.1f}%" if pd.notna(yoy_p) else "-"

            print(
                f"{year:<8} ${income:>11,.0f}  {yoy_d_str:<14} {yoy_p_str:<10} {note}"
            )

        avg_yoy_pct = inc["yoy_pct"].mean()
        print(f"\nAverage YoY Growth: {avg_yoy_pct:+.1f}%/year")

    # Population
    dem = load_historical("scott_county_iowa_demographics_historical_*.csv")
    if dem is not None:
        print("\n" + "=" * 80)
        print("POPULATION")
        print("=" * 80)

        dem = dem.sort_values("year").copy()
        dem["yoy"] = dem["Total population"].diff()
        dem["yoy_pct"] = dem["yoy"] / dem["Total population"].shift(1) * 100

        print(
            f"\n{'Year':<8} {'Population':<14} {'YoY Change':<14} {'YoY %':<10} {'Notes'}"
        )
        print("-" * 80)

        for _, row in dem.iterrows():
            year = int(row["year"])
            pop = row["Total population"]
            yoy = row["yoy"]
            yoy_pct = row["yoy_pct"]

            note = ""
            if pd.notna(yoy_pct):
                if yoy_pct > 1:
                    note = "Rapid growth"
                elif yoy_pct < 0:
                    note = "Population loss"

            yoy_str = f"{yoy:+,.0f}" if pd.notna(yoy) else "-"
            yoy_p_str = f"{yoy_pct:+.2f}%" if pd.notna(yoy_pct) else "-"

            print(f"{year:<8} {pop:>12,.0f}  {yoy_str:<14} {yoy_p_str:<10} {note}")

        avg_yoy = dem["yoy"].mean()
        avg_yoy_pct = dem["yoy_pct"].mean()
        print(
            f"\nAverage YoY Change: {avg_yoy:+,.0f} people/year ({avg_yoy_pct:+.2f}%)"
        )

    # Housing
    hou = load_historical("scott_county_iowa_housing_historical_*.csv")
    if hou is not None:
        print("\n" + "=" * 80)
        print("HOUSING")
        print("=" * 80)

        hou = hou.sort_values("year").copy()
        hou["yoy_dollars"] = hou["Median home value"].diff()
        hou["yoy_pct"] = hou["yoy_dollars"] / hou["Median home value"].shift(1) * 100

        print(f"\n{'Year':<8} {'Home Value':<16} {'YoY $':<16} {'YoY %':<10} {'Notes'}")
        print("-" * 80)

        for _, row in hou.iterrows():
            year = int(row["year"])
            value = row["Median home value"]
            yoy_d = row["yoy_dollars"]
            yoy_p = row["yoy_pct"]

            note = ""
            if pd.notna(yoy_p):
                if yoy_p > 5:
                    note = "Strong appreciation"
                elif yoy_p < 0:
                    note = "Depreciation"

            yoy_d_str = f"${yoy_d:+,.0f}" if pd.notna(yoy_d) else "-"
            yoy_p_str = f"{yoy_p:+.1f}%" if pd.notna(yoy_p) else "-"

            print(
                f"{year:<8} ${value:>13,.0f}   {yoy_d_str:<16} {yoy_p_str:<10} {note}"
            )

        avg_yoy_pct = hou["yoy_pct"].mean()
        print(f"\nAverage YoY Appreciation: {avg_yoy_pct:+.1f}%/year")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
    main()
    main()
    main()
    main()
