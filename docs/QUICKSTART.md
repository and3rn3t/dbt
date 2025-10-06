# Quick Start Guide 🚀

Welcome to your data science workspace! Everything is set up and ready to go.

## ✅ What's Ready

- **Virtual Environment**: Python 3.11.9 with 183+ packages installed
- **Tests**: 10/10 passing with 81% coverage
- **Utility Functions**: Data loading, saving, and validation helpers
- **Sample Data**: 5 CSV files ready for analysis
- **Notebooks**: 3 Jupyter notebooks ready to use
- **dbt Project**: Configured for data transformation

## 🎯 Start Here

### Option 1: Quick Data Analysis (Recommended)

Open one of your existing notebooks:

- **`notebooks/data_science_setup.ipynb`** - Setup examples and tutorials
- **`data_cleaning_pipeline.ipynb`** - Data cleaning workflows
- **`test_datagov_notebook.ipynb`** - Data.gov API examples

### Option 2: Use Python Directly

```powershell
# Set PYTHONPATH (important!)
$env:PYTHONPATH = "c:\git\dbt"

# Load and analyze data
c:/git/dbt/.venv/Scripts/python.exe -c "from scripts.utils import load_csv; df = load_csv('sample_sales_data.csv'); print(df.describe())"
```

### Option 3: Start Jupyter Lab

```powershell
# From the project root
c:/git/dbt/.venv/Scripts/python.exe -m jupyter lab
```

Then navigate to any `.ipynb` file and start analyzing!

## 📊 Your Sample Data

Located in `data/raw/`:

- `sample_sales_data.csv` - 1,000 rows of sales data
- `kzjm-xkqj_*.csv` - Seattle police data (multiple files)
- `nyc_311_*.csv` - NYC 311 service requests

## 🛠️ Utility Functions

Your new helper functions in `scripts/utils.py`:

```python
from scripts.utils import load_csv, save_csv, validate_dataframe

# Load data easily
df = load_csv("sample_sales_data.csv")

# Validate data
validate_dataframe(df, required_columns=["date", "sales"])

# Process data
df_clean = df.dropna()

# Save results
save_csv(df_clean, "cleaned_sales.csv", subfolder="processed", index=False)
```

## 🧪 Run Tests

```powershell
# Run all tests
pytest -v

# Run with coverage
pytest --cov=scripts --cov=tests

# Run specific test
pytest tests/test_utils.py -v
```

## 📝 Common Tasks

### Fetch New Data from Data.gov

```powershell
python scripts/fetch_data_gov.py
# or
python scripts/fetch_data_gov_v2.py
```

### Format Your Code

```powershell
black scripts/ tests/
isort scripts/ tests/
```

### Check Code Quality

```powershell
flake8 scripts/ tests/
```

## 🎓 Learning Resources

Check the `docs/` folder:

- `DATA_SCIENCE_GUIDE.md` - Best practices
- `DATA_GOV_GUIDE.md` - Using the Data.gov API
- `CONFIGURATION.md` - Project settings
- `QUICK_TOKEN_GUIDE.md` - API authentication

## 🔥 Pro Tips

1. **Always set PYTHONPATH** when running scripts:

   ```powershell
   $env:PYTHONPATH = "c:\git\dbt"
   ```

2. **Use utility functions** instead of repeating code:

   ```python
   from scripts.utils import load_csv, save_csv
   ```

3. **Write tests** for your functions:

   ```python
   # In tests/test_my_analysis.py
   def test_my_function():
       assert my_function() == expected_result
   ```

4. **Document in notebooks** with markdown cells:
   - Explain your reasoning
   - Document assumptions
   - Share insights

## 🐛 Troubleshooting

### "No module named 'scripts'"

```powershell
$env:PYTHONPATH = "c:\git\dbt"
```

### Jupyter won't start

```powershell
c:/git/dbt/.venv/Scripts/python.exe -m jupyter lab
```

### Import errors

Make sure you're in the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

## 🎉 You're All Set

Your workspace is configured, tested, and ready. Pick one of the options above and start analyzing!

**Recommended First Step**: Open `notebooks/data_science_setup.ipynb` in VS Code to see examples.

---

Need help? Check:

- `README.md` - Full documentation
- `SETUP_COMPLETE.md` - Setup details
- `.github/copilot-instructions.md` - Coding conventions
