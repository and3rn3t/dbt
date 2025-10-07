#!/usr/bin/env python3
"""Quick summary of Scott County Census data."""
from pathlib import Path

import pandas as pd

print("\n" + "=" * 80)
print("SCOTT COUNTY, IOWA - CENSUS DATA SUMMARY")
print("=" * 80)

files = sorted(Path("data/raw").glob("scott_county_iowa_*_2021_*.csv"))

print(f"\n✅ {len(files)} datasets downloaded\n")

for f in files:
    dataset_name = f.stem.split("_")[3].title()
    df = pd.read_csv(f)

    print(f"📊 {dataset_name}")
    print(f"   File: {f.name}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Size: {f.stat().st_size / 1024:.2f} KB")

    # Show key metrics
    if "education" in f.name:
        bach_col = "Bachelor's degree or higher (%)"
        if bach_col in df.columns:
            print(f"   → Bachelor's degree or higher: {df[bach_col].iloc[0]:.1f}%")

    elif "income" in f.name:
        if "Median household income" in df.columns:
            print(
                f"   → Median household income: ${df['Median household income'].iloc[0]:,.0f}"
            )
        if "Poverty rate (%)" in df.columns:
            print(f"   → Poverty rate: {df['Poverty rate (%)'].iloc[0]:.1f}%")

    elif "demographics" in f.name:
        if "Total population" in df.columns:
            print(f"   → Total population: {df['Total population'].iloc[0]:,.0f}")
        if "Median age" in df.columns:
            print(f"   → Median age: {df['Median age'].iloc[0]:.1f} years")

    elif "housing" in f.name:
        if "Median value (owner-occupied units)" in df.columns:
            print(
                f"   → Median home value: ${df['Median value (owner-occupied units)'].iloc[0]:,.0f}"
            )
        if "Owner occupied (%)" in df.columns:
            print(f"   → Homeownership rate: {df['Owner occupied (%)'].iloc[0]:.1f}%")

    elif "employment" in f.name:
        if "Unemployment rate (%)" in df.columns:
            print(f"   → Unemployment rate: {df['Unemployment rate (%)'].iloc[0]:.1f}%")
        if "Employed" in df.columns:
            print(f"   → Total employed: {df['Employed'].iloc[0]:,.0f}")

    print()

print("=" * 80)
print("🎯 Next Steps:")
print("=" * 80)
print("\n1. Open in Jupyter Lab for analysis:")
print("   jupyter lab")
print("\n2. Load all data:")
print("   df = pd.read_csv('data/raw/scott_county_iowa_education_2021_*.csv')")
print("\n3. Compare with NYC or other datasets")
print("\n4. Create visualizations and dashboards")
print()
print()
print()
print()
print()
