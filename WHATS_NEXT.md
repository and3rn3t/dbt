# What's Next? 🎯

You've successfully set up your data science workspace! Here's what to do next based on your goals:

## 🌟 **Recommended: Start Here**

### Option A: Interactive Tutorial (Best for Learning)

**Open:** `notebooks/data_science_setup.ipynb`

This notebook has:

- ✅ Working examples you can run immediately
- ✅ Visualization techniques (matplotlib, seaborn, plotly)
- ✅ Data analysis patterns
- ✅ Best practices demonstrated

**How:** Just click the file in VS Code Explorer → Run cells with Shift+Enter

---

## 🚀 **Quick Wins**

### Option B: Run Example Analysis

We just analyzed your sales data and found:

- 💰 **Total Sales:** $256,787.87
- 📊 **Top Category:** Electronics
- 🗺️ **Best Region:** West

**Try it yourself:**

```powershell
$env:PYTHONPATH = "c:\git\dbt"
c:/git/dbt/.venv/Scripts/python.exe scripts/example_analysis.py
```

**Modify it:**

- Edit `scripts/example_analysis.py`
- Change what metrics you calculate
- Try different visualizations

---

## 🔬 **Explore Different Datasets**

You have **7,150 rows** of data across 5 files:

### 1. Sample Sales Data (Learning-Friendly)

- **File:** `sample_sales_data.csv`
- **Size:** 1,000 rows, 8 columns
- **Best For:** Learning pandas, practicing visualization
- **Contains:** Sales transactions with products, regions, dates

```python
from scripts.utils import load_csv
df = load_csv("sample_sales_data.csv")
print(df.head())
```

### 2. NYC 311 Service Requests (Real-World)

- **File:** `nyc_311_20251005_121831.csv`
- **Size:** 1,000 rows, 12 columns
- **Best For:** Time series analysis, text analysis
- **Contains:** Government service requests with addresses, types, dates

### 3. Seattle Police Data (Larger Dataset)

- **Files:** 3 files with 50, 100, and 5,000 rows
- **Total:** 5,150 rows, 12 columns
- **Best For:** Data merging, geospatial analysis
- **Contains:** Police incident reports

**View all datasets:**

```powershell
python scripts/show_next_steps.py
```

---

## 📚 **Learn from Documentation**

All guides are in the `docs/` folder:

- **`DATA_SCIENCE_GUIDE.md`** - Best practices and patterns
- **`DATA_GOV_GUIDE.md`** - Fetch new datasets from Data.gov
- **`CONFIGURATION.md`** - Project setup details
- **`QUICK_TOKEN_GUIDE.md`** - API authentication

---

## 🛠️ **Create Your Own Analysis**

### Start a New Notebook

1. Right-click in `notebooks/` folder
2. New File → `my_analysis.ipynb`
3. Start coding!

### Use the Utility Functions

```python
from scripts.utils import load_csv, save_csv, validate_dataframe

# Load data
df = load_csv("sample_sales_data.csv")

# Analyze
revenue_by_category = df.groupby('category')['sales'].sum()

# Save results
save_csv(revenue_by_category.to_frame(), "revenue_summary.csv", subfolder="processed")
```

---

## 🎨 **Try These Quick Tasks**

### Task 1: Sales by Region (5 minutes)

```python
from scripts.utils import load_csv
import matplotlib.pyplot as plt

df = load_csv("sample_sales_data.csv")
df.groupby('region')['sales'].sum().plot(kind='bar')
plt.title('Sales by Region')
plt.show()
```

### Task 2: Top Products (3 minutes)

```python
from scripts.utils import load_csv

df = load_csv("sample_sales_data.csv")
top_products = df.groupby('product_id')['sales'].sum().sort_values(ascending=False).head(5)
print(top_products)
```

### Task 3: Time Series Analysis (10 minutes)

```python
from scripts.utils import load_csv
import pandas as pd

df = load_csv("sample_sales_data.csv")
df['date'] = pd.to_datetime(df['date'])
daily_sales = df.groupby('date')['sales'].sum()
daily_sales.plot(figsize=(12, 6))
```

---

## 🔄 **What We Set Up For You**

✅ Virtual environment with 183 packages
✅ Jupyter notebooks ready to run
✅ Utility functions for easy data loading
✅ 10 unit tests passing
✅ Code formatting configured
✅ Sample datasets loaded
✅ dbt project initialized
✅ Complete documentation

---

## 💡 **My Recommendation**

**If you're new to data science:**
→ Start with `notebooks/data_science_setup.ipynb`

**If you want quick results:**
→ Run and modify `scripts/example_analysis.py`

**If you want to explore:**
→ Run `python scripts/show_next_steps.py` to see all datasets

**If you're ready to create:**
→ Start a new notebook in `notebooks/` and use utility functions

---

## 🆘 **Need Help?**

- Check `QUICKSTART.md` for common commands
- Review `README.md` for full documentation
- Look at examples in `notebooks/data_science_setup.ipynb`
- Run `pytest -v` to ensure everything works

---

## 🎯 **Action Item**

**Choose ONE thing to do right now:**

1. [ ] Click `notebooks/data_science_setup.ipynb` in VS Code
2. [ ] Run `python scripts/example_analysis.py`
3. [ ] Open `sample_sales_data.csv` and explore
4. [ ] Create your own notebook
5. [ ] Read the documentation

**Don't overthink it - just pick one and start!** 🚀
