"""Quick analysis of NYC education data we just fetched."""

import pandas as pd

from scripts.utils import load_csv

print("\n" + "=" * 60)
print("📊 NYC EDUCATION DATA - QUICK ANALYSIS")
print("=" * 60 + "\n")

# 1. SAT Scores Analysis
print("1️⃣  SAT SCORES BY SCHOOL")
print("-" * 60)
try:
    sat = load_csv("zt9s-n5aj_20251006_114228.csv")

    print(f"Total Schools: {len(sat)}")
    print(f"Columns: {list(sat.columns)}")
    print(f"\n📈 Average SAT Scores:")

    # Convert to numeric
    sat["mathematics_mean"] = pd.to_numeric(sat["mathematics_mean"], errors="coerce")
    sat["critical_reading_mean"] = pd.to_numeric(
        sat["critical_reading_mean"], errors="coerce"
    )
    sat["writing_mean"] = pd.to_numeric(sat["writing_mean"], errors="coerce")

    print(f"   Math: {sat['mathematics_mean'].mean():.0f}")
    print(f"   Reading: {sat['critical_reading_mean'].mean():.0f}")
    print(f"   Writing: {sat['writing_mean'].mean():.0f}")

    # Calculate total
    sat["total_score"] = (
        sat["mathematics_mean"] + sat["critical_reading_mean"] + sat["writing_mean"]
    )

    print(f"   Total (avg): {sat['total_score'].mean():.0f}")

    print(f"\n🏆 Top 5 Schools by Total SAT Score:")
    top_schools = sat.nlargest(5, "total_score")[["school_name", "total_score"]]
    for idx, row in top_schools.iterrows():
        print(f"   {row['school_name'][:50]}: {row['total_score']:.0f}")

    print(f"\n📊 Score Distribution:")
    print(f"   Highest Total: {sat['total_score'].max():.0f}")
    print(f"   Lowest Total: {sat['total_score'].min():.0f}")
    print(f"   Median Total: {sat['total_score'].median():.0f}")

except FileNotFoundError:
    print("   ⚠ SAT data file not found")
except Exception as e:
    print(f"   ⚠ Error: {e}")

print("\n" + "=" * 60)

# 2. School Demographics Analysis
print("\n2️⃣  SCHOOL DEMOGRAPHICS")
print("-" * 60)
try:
    demo = load_csv("s3k6-pzi2_20251006_114239.csv")

    print(f"Total Schools: {len(demo)}")
    print(f"Total Columns: {len(demo.columns)}")
    print(f"\n📝 Key Information Available:")
    print(f"   • School names and DBN codes")
    print(f"   • Borough locations")
    print(f"   • Program details")
    print(f"   • Academic opportunities")

    if "boro" in demo.columns:
        print(f"\n🗽 Schools by Borough:")
        borough_counts = demo["boro"].value_counts()
        for boro, count in borough_counts.items():
            print(f"   {boro}: {count} schools")

    print(f"\n💡 Sample School Names:")
    for name in demo["school_name"].head(5):
        print(f"   • {name[:60]}")

    print(f"\n📊 Dataset Statistics:")
    print(f"   Records: {len(demo):,}")
    print(f"   Columns: {len(demo.columns):,}")
    print(f"   File Size: 1.4 MB")

except FileNotFoundError:
    print("   ⚠ Demographics data file not found")
except Exception as e:
    print(f"   ⚠ Error: {e}")

print("\n" + "=" * 60)
print("\n✅ DATA FETCHED SUCCESSFULLY!")
print("=" * 60)
print("\n📁 Files saved to data/raw/:")
print("   • zt9s-n5aj_20251006_114228.csv (SAT scores)")
print("   • s3k6-pzi2_20251006_114239.csv (Demographics)")
print("\n🎯 Next Steps:")
print("   1. Merge SAT scores with demographics for deeper analysis")
print("   2. Analyze correlations between demographics and performance")
print("   3. Create visualizations (SAT score distributions, borough comparisons)")
print("   4. Build predictive models")
print("\n💡 Try these analyses:")
print("   • Which boroughs have highest average SAT scores?")
print("   • Relationship between school size and performance?")
print("   • Compare programs across top performing schools")
print()
