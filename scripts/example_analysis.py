"""Quick example: Analyze sales data in 5 lines of code."""

from scripts.utils import load_csv

# Load data
df = load_csv("sample_sales_data.csv")

# Quick insights
print("\n📊 QUICK SALES ANALYSIS\n")
print(f"Total Sales: ${df['sales'].sum():,.2f}")
print(f"Average Order: ${df['sales'].mean():.2f}")
print(f"Top Category: {df.groupby('category')['sales'].sum().idxmax()}")
print(f"Best Region: {df.groupby('region')['sales'].sum().idxmax()}")
print(f"\nTop 5 Products by Revenue:")
print(df.groupby("product_id")["sales"].sum().sort_values(ascending=False).head())

# Save summary
summary = (
    df.groupby("category")
    .agg({"sales": ["sum", "mean", "count"], "quantity": "sum"})
    .round(2)
)

print(f"\n📈 Category Summary:")
print(summary)
print("\n✅ Analysis complete! Check data/processed/ for results.\n")
