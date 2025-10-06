# Data Science Workspace Setup Guide

## 🎯 Overview

This workspace is now configured for data science and working with datasets, including:

- Python data science libraries
- Jupyter notebooks support
- CSV/TSV file handling with Rainbow CSV
- Data Wrangler for interactive data exploration
- DBT integration for data transformation

---

## 📦 Installed Extensions

### Core Data Science Extensions

- **Python** - Full Python language support
- **Jupyter** - Interactive notebooks
- **Jupyter Notebook Renderers** - Rich output rendering
- **Data Wrangler** - Interactive data viewing and cleaning
- **Rainbow CSV** - CSV/TSV syntax highlighting and SQL queries

---

## 🚀 Getting Started

### 1. Install Python Packages

```powershell
# Install all data science dependencies
pip install -r requirements-datascience.txt

# Or install specific packages
pip install pandas numpy matplotlib seaborn plotly
```

### 2. Open the Setup Notebook

1. Navigate to `notebooks/data_science_setup.ipynb`
2. Click to open it in the Jupyter notebook editor
3. Select your Python kernel (Python 3.x)
4. Run all cells to verify your setup

### 3. Explore Sample Data

The setup notebook creates sample sales data in `data/raw/sample_sales_data.csv`

---

## 📊 Working with Data

### Loading Data in Jupyter Notebooks

```python
import pandas as pd
from pathlib import Path

# Define paths
PROJECT_ROOT = Path.cwd().parent
DATA_DIR = PROJECT_ROOT / 'data'

# Load CSV
df = pd.read_csv(DATA_DIR / 'raw' / 'your_file.csv')

# Load Excel
df = pd.read_excel(DATA_DIR / 'raw' / 'your_file.xlsx')

# Load from URL
df = pd.read_csv('https://example.com/data.csv')
```

### Using Data Wrangler

1. Right-click any CSV file in the Explorer
2. Select "Open with Data Wrangler"
3. Perform interactive data cleaning and transformation
4. Export the generated code to your notebook

### CSV/TSV with Rainbow CSV

- Automatic syntax highlighting for CSV/TSV files
- Hover over cells to see column names
- Run SQL-like queries on CSV files (F5)
- Align columns for better readability

---

## 📁 Project Structure

```
dbt/
├── data/
│   ├── raw/              # Original, immutable data
│   ├── processed/        # Cleaned, transformed data
│   ├── staging/          # Intermediate data
│   └── external/         # Data from external sources
├── notebooks/
│   ├── data_science_setup.ipynb    # This setup notebook
│   └── explore_data.md             # Exploration notebook
├── scripts/
│   └── fetch_data_gov.py          # Data fetching scripts
├── dbt_project/          # DBT models and configuration
└── requirements-datascience.txt   # Python dependencies
```

---

## 🔧 Common Tasks

### Create a New Jupyter Notebook

1. In VS Code, press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
2. Type "Create: New Jupyter Notebook"
3. Start coding!

### Basic Data Analysis Template

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('path/to/data.csv')

# Explore
print(df.head())
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Visualize
df['column'].hist()
plt.show()

# Save processed data
df.to_csv('data/processed/cleaned_data.csv', index=False)
```

### Integrating with DBT

After processing data in notebooks, use it in DBT:

```python
# Save to staging area for DBT
processed_df.to_csv(
    DATA_DIR / 'staging' / 'processed_sales.csv',
    index=False
)
```

Then reference it in your DBT models:

```sql
-- models/staging/stg_processed_sales.sql
SELECT * FROM {{ source('staging', 'processed_sales') }}
```

---

## 🎨 Visualization Examples

### Matplotlib

```python
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'])
plt.title('Time Series')
plt.xlabel('Date')
plt.ylabel('Value')
plt.show()
```

### Seaborn

```python
sns.set_style('whitegrid')
sns.boxplot(data=df, x='category', y='value')
plt.show()
```

### Plotly (Interactive)

```python
import plotly.express as px

fig = px.scatter(df, x='x_col', y='y_col', color='category',
                 size='size_col', hover_data=['info'])
fig.show()
```

---

## 🛠️ Keyboard Shortcuts

### Jupyter Notebooks

- `Shift+Enter` - Run cell and move to next
- `Ctrl+Enter` - Run cell
- `A` - Insert cell above
- `B` - Insert cell below
- `DD` - Delete cell
- `M` - Change to Markdown
- `Y` - Change to Code

### VS Code

- `Ctrl+Shift+P` - Command palette
- `Ctrl+` - Open terminal
- `Ctrl+B` - Toggle sidebar
- `Ctrl+Shift+F` - Search across files

---

## 📚 Resources

### Documentation

- [Pandas](https://pandas.pydata.org/docs/)
- [NumPy](https://numpy.org/doc/)
- [Matplotlib](https://matplotlib.org/stable/contents.html)
- [Seaborn](https://seaborn.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Data Wrangler](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler)

### Learning Resources

- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Jupyter Notebook Tutorial](https://jupyter.org/try)

---

## 🐛 Troubleshooting

### Python Kernel Not Found

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose your Python installation

### Package Import Errors

```powershell
# Verify package installation
pip list

# Reinstall if needed
pip install --upgrade pandas numpy matplotlib
```

### Jupyter Not Starting

```powershell
# Install Jupyter kernel
pip install ipykernel
python -m ipykernel install --user
```

---

## 💡 Tips & Best Practices

1. **Use Virtual Environments**: Keep project dependencies isolated
2. **Version Control Data**: Use `.gitignore` for large data files
3. **Document Your Analysis**: Use Markdown cells in notebooks
4. **Save Intermediate Results**: Don't recompute expensive operations
5. **Use Relative Paths**: Makes your code portable
6. **Test with Small Samples**: Work with subsets before processing full datasets
7. **Profile Your Code**: Use `%%time` magic command for performance

---

## 🔄 Next Steps

1. ✅ Review the setup notebook: `notebooks/data_science_setup.ipynb`
2. ✅ Try Data Wrangler on `data/raw/sample_sales_data.csv`
3. ✅ Create your first analysis notebook
4. ✅ Install additional packages as needed
5. ✅ Integrate findings with DBT models

---

**Happy Data Science! 🚀📊**
