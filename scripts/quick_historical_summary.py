from pathlib import Path

import pandas as pd

print("\n" + "=" * 80)
print("SCOTT COUNTY, IOWA - HISTORICAL DATA SUMMARY")
print("=" * 80 + "\n")

files = list(Path("data/raw").glob("scott_county_iowa_*_historical_*.csv"))

for f in sorted(files):
    df = pd.read_csv(f)
    dataset = f.stem.split("_")[3]
    years = f"{int(df['year'].min())}-{int(df['year'].max())}"
    print(f"{dataset.title():15} {len(df):2} years  ({years})")

print("\n" + "=" * 80)
print("QUICK STATS")
print("=" * 80 + "\n")

# Education
edu = pd.read_csv(next(Path("data/raw").glob("*education_historical_*.csv")))
first_edu = edu[edu["year"] == edu["year"].min()][
    "Bachelor's degree or higher (%)"
].values[0]
last_edu = edu[edu["year"] == edu["year"].max()][
    "Bachelor's degree or higher (%)"
].values[0]
print(
    f"Education (Bachelor's+): {first_edu:.1f}% -> {last_edu:.1f}% ({last_edu-first_edu:+.1f} pts)"
)

# Income
inc = pd.read_csv(next(Path("data/raw").glob("*income_historical_*.csv")))
first_inc = inc[inc["year"] == inc["year"].min()]["Median household income"].values[0]
last_inc = inc[inc["year"] == inc["year"].max()]["Median household income"].values[0]
print(
    f"Income: ${first_inc:,.0f} -> ${last_inc:,.0f} ({(last_inc-first_inc)/first_inc*100:+.1f}%)"
)

# Population
pop = pd.read_csv(next(Path("data/raw").glob("*demographics_historical_*.csv")))
first_pop = pop[pop["year"] == pop["year"].min()]["Total population"].values[0]
last_pop = pop[pop["year"] == pop["year"].max()]["Total population"].values[0]
print(
    f"Population: {first_pop:,.0f} -> {last_pop:,.0f} ({(last_pop-first_pop)/first_pop*100:+.1f}%)"
)

# Housing
hs = pd.read_csv(next(Path("data/raw").glob("*housing_historical_*.csv")))
first_hs = hs[hs["year"] == hs["year"].min()]["Median home value"].values[0]
last_hs = hs[hs["year"] == hs["year"].max()]["Median home value"].values[0]
print(
    f"Home Value: ${first_hs:,.0f} -> ${last_hs:,.0f} ({(last_hs-first_hs)/first_hs*100:+.1f}%)"
)

print("\n" + "=" * 80)
print("\n" + "=" * 80)
print("\n" + "=" * 80)
print("\n" + "=" * 80)
print("\n" + "=" * 80)
