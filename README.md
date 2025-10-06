# Data Science & Analytics Project

A comprehensive data science and analytics workspace combining Python analysis, dbt data transformation, and interactive notebooks.

## 🚀 Quick Start

### 1. Activate Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Verify Installation

```powershell
# Check Python version
python --version  # Should be 3.11.9

# Run tests
pytest

# Check installed packages
pip list
```

### 3. Start Jupyter Lab

```powershell
jupyter lab
```

## 📁 Project Structure

```
dbt/
├── data/                          # Data storage
│   ├── raw/                       # Original, immutable data
│   ├── processed/                 # Cleaned, transformed data
│   ├── staging/                   # Intermediate data
│   └── external/                  # External data sources
├── notebooks/                     # Jupyter notebooks for analysis
│   └── data_science_setup.ipynb  # Setup and examples
├── scripts/                       # Python scripts for automation
│   ├── fetch_data_gov.py         # Data fetching utilities
│   ├── fetch_data_gov_v2.py      # Enhanced data fetching
│   └── utils.py                  # Common utility functions
├── dbt_project/                  # dbt models and configuration
│   ├── models/                   # SQL transformation models
│   │   ├── staging/              # Staging layer models
│   │   └── marts/                # Business logic layer
│   ├── seeds/                    # CSV files to load
│   └── dbt_project.yml           # dbt configuration
├── tests/                        # Test files
├── templates/                    # Code templates
├── docs/                         # Documentation
└── .venv/                        # Virtual environment
```

## 🛠️ Development Workflow

### Working with Data

```python
from scripts.utils import load_csv, save_csv, validate_dataframe

# Load raw data
df = load_csv("sample_sales_data.csv")

# Validate data
validate_dataframe(df, required_columns=["id", "amount"])

# Process data
df_clean = df.dropna()

# Save processed data
save_csv(df_clean, "cleaned_sales.csv", subfolder="processed", index=False)
```

### Code Formatting

```powershell
# Format all code
black .
isort .

# Check linting
flake8 .
```

### Running Tests

```powershell
# Run all tests
pytest

# Run specific test file
pytest tests/test_utils.py

# Run with coverage report
pytest --cov=. --cov-report=html
```

## 📊 dbt Setup (Optional)

If you're using dbt for data transformation:

### 1. Configure Database

Update `.env` with your database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

### 2. Set up dbt Profile

Copy the profile to your home directory:

```powershell
# Create .dbt directory in home folder
New-Item -ItemType Directory -Force -Path "$HOME\.dbt"

# Copy profile
Copy-Item dbt_project\profiles.yml "$HOME\.dbt\profiles.yml"
```

Or set the environment variable:

```powershell
$env:DBT_PROFILES_DIR = "c:\git\dbt\dbt_project"
```

### 3. Run dbt Commands

```powershell
# Navigate to dbt project
cd dbt_project

# Run all models
dbt run

# Test data quality
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

## 📚 Available Tools

### Python Libraries

- **Data Analysis**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Scientific Computing**: scipy
- **File Support**: openpyxl (Excel), pyarrow (Parquet)
- **Development**: black, flake8, pytest, isort

### Notebooks

- Jupyter Lab for interactive analysis
- Pre-configured with common imports
- Examples in `notebooks/data_science_setup.ipynb`

## 🔒 Security

- ✅ `.env` file is in `.gitignore` (never commit secrets!)
- ✅ Use `.env.example` as a template
- ✅ Store API keys and credentials in `.env`

## 📖 Documentation

Check the `docs/` folder for detailed guides:

- `DATA_SCIENCE_GUIDE.md` - Data science best practices
- `DATA_GOV_GUIDE.md` - Using data.gov API
- `CONFIGURATION.md` - Project configuration
- `API_TOKEN_GUIDE.md` - API authentication

## 🧪 Testing

All tests passed! ✅

- 10 tests in test suite
- 81% coverage on utility functions
- Tests for data validation, path handling, and DataFrame operations

## 💡 Tips

1. **Always activate the virtual environment** before working
2. **Format code before committing**: `black . && isort .`
3. **Run tests frequently**: `pytest`
4. **Document your analyses** in notebooks with markdown cells
5. **Use the utils module** for common data operations

## 🐛 Troubleshooting

### Jupyter Kernel Issues

```powershell
python -m ipykernel install --user --name=dbt-env
```

### Import Errors

Make sure you're in the project root and the virtual environment is activated.

### dbt Connection Issues

1. Verify `.env` has correct database credentials
2. Test database connection manually
3. Check `profiles.yml` configuration

## 📝 Next Steps

1. ✅ Virtual environment created and activated
2. ✅ All dependencies installed
3. ✅ Tests passing
4. ✅ Code formatted
5. ⏭️ Start exploring notebooks
6. ⏭️ Configure dbt (if needed)
7. ⏭️ Add your data to `data/raw/`
8. ⏭️ Begin analysis!

---

**Happy Analyzing! 📊🐍**

For questions or issues, check the documentation in `docs/` or the `.github/copilot-instructions.md` file.
