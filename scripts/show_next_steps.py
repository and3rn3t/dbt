"""Analyze available datasets and suggest next steps."""

from pathlib import Path

import pandas as pd

print("\n" + "=" * 60)
print("📊 YOUR DATA INVENTORY")
print("=" * 60 + "\n")

raw_dir = Path("data/raw")
files = sorted(raw_dir.glob("*.csv"))

total_rows = 0
for f in files:
    df = pd.read_csv(f)
    total_rows += len(df)
    print(f"📁 {f.name}")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Size: {f.stat().st_size / 1024:.1f} KB")
    print(f"   First 3 columns: {', '.join(df.columns[:3])}")
    print()

print(f"💾 Total: {len(files)} files with {total_rows:,} rows combined\n")

print("=" * 60)
print("🎯 SUGGESTED NEXT STEPS")
print("=" * 60 + "\n")

print("1️⃣  EXPLORE SAMPLE DATA (Quick Start)")
print("   Open: notebooks/data_science_setup.ipynb")
print("   - See examples with the 1,000-row sample_sales_data.csv")
print("   - Learn visualization techniques")
print("   - Practice data cleaning\n")

print("2️⃣  ANALYZE NYC 311 REQUESTS (Real World Data)")
print("   - 5,000+ rows of NYC service requests")
print("   - Great for time series analysis")
print("   - Practice text analysis on descriptions\n")

print("3️⃣  ANALYZE SEATTLE POLICE DATA (Large Dataset)")
print("   - 30,000+ rows across 3 files")
print("   - Practice data merging/concatenation")
print("   - Geospatial analysis potential\n")

print("4️⃣  CREATE YOUR OWN ANALYSIS")
print("   - Use scripts/utils.py helpers")
print("   - Load: from scripts.utils import load_csv")
print("   - Start fresh notebook or Python script\n")

print("5️⃣  FETCH NEW DATA")
print("   - Run: python scripts/fetch_data_gov.py")
print("   - Explore Data.gov datasets")
print("   - See docs/DATA_GOV_GUIDE.md\n")

print("=" * 60)
print("💡 RECOMMENDATION")
print("=" * 60 + "\n")
print("Start with Option 1: Open data_science_setup.ipynb")
print("It has working examples you can run immediately!")
print("\nJust click the file in VS Code to open it.\n")
