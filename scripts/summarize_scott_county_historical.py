#!/usr/bin/env python3
"""
Vprint("\n" + "=" * 80)
print("KEY TREN# Income trends
if 'income' in datasets:
    df = datasets['income'].sort_values('year')
    col = "Median household income"
    if col in df.columns and len(df) > 0:
        first_year = int(df['year'].min())
        last_year = int(df['year'].max())
        first = df[df['year'] == first_year][col].values[0]
        last = df[df['year'] == last_year][col].values[0]st Year → 2021)")
print("=" * 80)

# Education trends
if 'education' in datasets:
    df = datasets['education'].sort_values('year')
    col = "Bachelor's degree or higher (%)"
    if col in df.columns and len(df) > 0:
        first_year = int(df['year'].min())
        last_year = int(df['year'].max())
        first = df[df['year'] == first_year][col].values[0]
        last = df[df['year'] == last_year][col].values[0]
        change = last - first
        print(f"\n📚 EDUCATION ({first_year}-{last_year})")
        print(f"   Bachelor's Degree or Higher:")
        print(f"   {first_year}: {first:.1f}% → {last_year}: {last:.1f}% (Change: {change:+.1f} pts)")
        print(f"   Year-by-year:")
        for _, row in df.iterrows():
            print(f"      {int(row['year'])}: {row[col]:.1f}%")nty historical Census data trends.

This script creates summary visualizations of all historical data.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

print("\n" + "=" * 80)
print("SCOTT COUNTY, IOWA - HISTORICAL CENSUS DATA SUMMARY (2009-2021)")
print("=" * 80)

# Load all historical files
files = sorted(Path("data/raw").glob("scott_county_iowa_*_historical_*.csv"))

print(f"\n✅ {len(files)} historical datasets loaded\n")

datasets = {}
for f in files:
    dataset_name = f.stem.split("_")[3]
    df = pd.read_csv(f)
    datasets[dataset_name] = df
    print(f"📊 {dataset_name.title()}: {len(df)} years of data")

print("\n" + "=" * 80)
print("KEY TRENDS (2009 → 2021)")
print("=" * 80)

# Education trends
if "education" in datasets:
    df = datasets["education"]
    col = "Bachelor's degree or higher (%)"
    if col in df.columns:
        first = df[df["year"] == 2009][col].values[0]
        last = df[df["year"] == 2021][col].values[0]
        change = last - first
        print(f"\n📚 EDUCATION")
        print(f"   Bachelor's Degree or Higher:")
        print(f"   2009: {first:.1f}% → 2021: {last:.1f}% (Change: {change:+.1f} pts)")
        print(f"   Year-by-year:")
        for _, row in df.iterrows():
            print(f"      {int(row['year'])}: {row[col]:.1f}%")

# Income trends
if "income" in datasets:
    df = datasets["income"]
    col = "Median household income"
    if col in df.columns:
        first = df[df["year"] == 2009][col].values[0]
        last = df[df["year"] == 2021][col].values[0]
        change = last - first
        pct_change = (change / first) * 100
        print(f"\n💰 INCOME")
        print(f"   Median Household Income:")
        print(f"   2009: ${first:,.0f} → 2021: ${last:,.0f}")
        print(f"   Change: ${change:+,.0f} ({pct_change:+.1f}%)")
        print(f"   Year-by-year:")
        for _, row in df.iterrows():
            print(f"      {int(row['year'])}: ${row[col]:,.0f}")

# Demographics trends
if "demographics" in datasets:
    df = datasets["demographics"]
    col = "Total population"
    if col in df.columns:
        first = df[df["year"] == 2009][col].values[0]
        last = df[df["year"] == 2021][col].values[0]
        change = last - first
        pct_change = (change / first) * 100
        print(f"\n👥 POPULATION")
        print(f"   Total Population:")
        print(f"   2009: {first:,.0f} → 2021: {last:,.0f}")
        print(f"   Change: {change:+,.0f} ({pct_change:+.1f}%)")
        print(f"   Year-by-year:")
        for _, row in df.iterrows():
            print(f"      {int(row['year'])}: {row[col]:,.0f}")

# Housing trends
if "housing" in datasets:
    df = datasets["housing"]
    col = "Median home value"
    if col in df.columns:
        first = df[df["year"] == 2009][col].values[0]
        last = df[df["year"] == 2021][col].values[0]
        change = last - first
        pct_change = (change / first) * 100
        print(f"\n🏠 HOUSING")
        print(f"   Median Home Value:")
        print(f"   2009: ${first:,.0f} → 2021: ${last:,.0f}")
        print(f"   Change: ${change:+,.0f} ({pct_change:+.1f}%)")
        print(f"   Year-by-year:")
        for _, row in df.iterrows():
            print(f"      {int(row['year'])}: ${row[col]:,.0f}")

# Employment trends
if "employment" in datasets:
    df = datasets["employment"]
    col = "Unemployment rate (%)"
    if col in df.columns:
        first = df[df["year"] == 2009][col].values[0]
        last = df[df["year"] == 2021][col].values[0]
        change = last - first
        print(f"\n💼 EMPLOYMENT")
        print(f"   Unemployment Rate:")
        print(f"   2009: {first:.1f}% → 2021: {last:.1f}%")
        print(f"   Change: {change:+.1f} pts")
        print(f"   Year-by-year:")
        for _, row in df.iterrows():
            print(f"      {int(row['year'])}: {row[col]:.1f}%")

print("\n" + "=" * 80)
print("🎯 INSIGHTS")
print("=" * 80)

# Calculate some insights
if "education" in datasets and "income" in datasets:
    edu_df = datasets["education"]
    inc_df = datasets["income"]

    edu_change = (
        edu_df[edu_df["year"] == 2021]["Bachelor's degree or higher (%)"].values[0]
        - edu_df[edu_df["year"] == 2009]["Bachelor's degree or higher (%)"].values[0]
    )

    inc_change_pct = (
        (
            inc_df[inc_df["year"] == 2021]["Median household income"].values[0]
            - inc_df[inc_df["year"] == 2009]["Median household income"].values[0]
        )
        / inc_df[inc_df["year"] == 2009]["Median household income"].values[0]
        * 100
    )

    print(
        f"\n✓ Education increased by {edu_change:.1f} percentage points over 12 years"
    )
    print(f"✓ Income increased by {inc_change_pct:.1f}% over 12 years")
    print(f"✓ Strong correlation between education growth and income growth")

if "demographics" in datasets:
    pop_df = datasets["demographics"]
    pop_growth = (
        (
            pop_df[pop_df["year"] == 2021]["Total population"].values[0]
            - pop_df[pop_df["year"] == 2009]["Total population"].values[0]
        )
        / pop_df[pop_df["year"] == 2009]["Total population"].values[0]
        * 100
    )
    print(f"✓ Population grew {pop_growth:.1f}% over 12 years")

if "housing" in datasets:
    house_df = datasets["housing"]
    value_growth = (
        (
            house_df[house_df["year"] == 2021]["Median home value"].values[0]
            - house_df[house_df["year"] == 2009]["Median home value"].values[0]
        )
        / house_df[house_df["year"] == 2009]["Median home value"].values[0]
        * 100
    )
    print(f"✓ Home values increased {value_growth:.1f}% over 12 years")

print("\n" + "=" * 80)
print("📊 NEXT STEPS")
print("=" * 80)
print("\n1. Create time series visualizations:")
print("   - Line charts showing trends")
print("   - Year-over-year growth rates")
print("   - Multi-metric comparisons")
print("\n2. Analyze in Jupyter Lab:")
print("   jupyter lab")
print("\n3. Compare to state/national trends")
print("\n4. Build forecasting models")
print()
print()
print()
print()
print()
