# Workspace Context for AI Assistants

This document provides additional context for AI coding assistants (GitHub Copilot, etc.) to better understand this workspace.

## Project Context

### What We're Building

A **data analytics and transformation pipeline** that:

- Ingests data from various sources (APIs, databases, files)
- Transforms and cleans data using dbt
- Analyzes data using Python and Jupyter notebooks
- Visualizes insights using matplotlib, seaborn, and plotly
- Potentially builds ML models for predictions

### Target Users

- Data analysts
- Data scientists
- Data engineers
- Business intelligence teams

### Key Use Cases

1. **ETL Pipeline**: Extract data → Transform with dbt → Load for analysis
2. **Exploratory Analysis**: Use Jupyter notebooks to explore and visualize data
3. **Reporting**: Generate insights and dashboards
4. **Data Quality**: Validate and test data transformations

## Current State

### What's Set Up ✅

- Python 3.11 environment with data science libraries
- dbt project structure with staging and marts layers
- Jupyter notebook environment with sample data
- Git configuration with proper .gitignore
- Code quality tools (black, flake8, pytest)
- Documentation and templates

### Sample Data Available

- `data/raw/sample_sales_data.csv` - 1,000 sales transactions
  - Columns: date, product_id, category, sales, quantity, customer_age, region, satisfaction_score
  - Use this for examples and testing

### dbt Seeds

- `dbt_project/seeds/example_seed_data.csv` - Example seed data

## Common Tasks & Patterns

### Task 1: Adding a New Data Source

```python
# 1. Create a fetch script in scripts/
# scripts/fetch_new_source.py
from pathlib import Path
import pandas as pd
import requests

def fetch_data(api_url: str) -> pd.DataFrame:
    """Fetch data from API."""
    response = requests.get(api_url)
    data = response.json()
    return pd.DataFrame(data)

def save_raw_data(df: pd.DataFrame, filename: str) -> None:
    """Save to raw data directory."""
    path = Path(__file__).parent.parent / 'data' / 'raw' / filename
    df.to_csv(path, index=False)

if __name__ == '__main__':
    df = fetch_data('https://api.example.com/data')
    save_raw_data(df, f'{pd.Timestamp.now().date()}_source_data.csv')
```

```sql
-- 2. Create dbt staging model
-- dbt_project/models/staging/stg_new_source.sql
with source as (
    select * from {{ source('raw', 'new_source') }}
),

cleaned as (
    select
        id,
        lower(trim(name)) as name,
        cast(amount as decimal(10,2)) as amount,
        to_timestamp(created_at) as created_at
    from source
    where amount > 0
)

select * from cleaned
```

```yaml
# 3. Add to sources.yml
# dbt_project/models/staging/sources.yml
sources:
  - name: raw
    tables:
      - name: new_source
        description: "Description of the new data source"
```

### Task 2: Exploratory Data Analysis

```python
# Create new notebook: notebooks/analysis_<topic>.ipynb

# Standard notebook structure:
# 1. Setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROJECT_ROOT = Path.cwd().parent
%matplotlib inline

# 2. Load data
df = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'data.csv')

# 3. Initial exploration
print(f"Shape: {df.shape}")
print(f"\nInfo:")
df.info()
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nSummary:\n{df.describe()}")

# 4. Visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# ... add plots

# 5. Analysis and insights
# Document findings in markdown cells

# 6. Save results if needed
df_processed.to_csv(PROJECT_ROOT / 'data' / 'processed' / 'result.csv')
```

### Task 3: Creating a dbt Mart

```sql
-- dbt_project/models/marts/mart_sales_summary.sql
{{ config(materialized='table') }}

with daily_sales as (
    select
        date_trunc('day', order_date) as sale_date,
        product_id,
        sum(quantity) as total_quantity,
        sum(amount) as total_amount,
        count(distinct customer_id) as customer_count
    from {{ ref('stg_sales_orders') }}
    where status = 'completed'
    group by 1, 2
),

with_metrics as (
    select
        *,
        total_amount / nullif(total_quantity, 0) as avg_price,
        total_amount / nullif(customer_count, 0) as revenue_per_customer
    from daily_sales
)

select * from with_metrics
```

```yaml
# dbt_project/models/marts/marts.yml
models:
  - name: mart_sales_summary
    description: "Daily sales metrics by product"
    columns:
      - name: sale_date
        description: "Date of sale"
        tests:
          - not_null
      - name: total_amount
        description: "Total revenue"
        tests:
          - not_null
```

## Data Flow

```
External Sources (APIs, DBs, Files)
    ↓
scripts/fetch_*.py  → Download to data/raw/
    ↓
dbt staging models  → Clean & standardize
    ↓
dbt mart models     → Business logic & aggregations
    ↓
notebooks/          → Analysis & visualization
    ↓
Insights & Reports
```

## Important Conventions

### Variable Naming

```python
# DataFrame variables
df_customers        # Original data
df_cleaned          # After cleaning
df_aggregated       # After aggregation
df_final           # Final result

# Path variables
PROJECT_ROOT       # Project root directory
DATA_DIR          # data/ directory
RAW_DATA_DIR      # data/raw/
PROCESSED_DIR     # data/processed/
```

### Function Naming

```python
# Data loading
load_raw_data()
read_processed_data()
fetch_from_api()

# Data transformation
clean_dataframe()
transform_data()
aggregate_metrics()

# Data saving
save_processed_data()
export_to_csv()
write_results()
```

### SQL Naming

```sql
-- CTEs (Common Table Expressions)
source            -- Raw source data
renamed           -- After renaming columns
cleaned           -- After cleaning/filtering
aggregated        -- After aggregation
final             -- Final output

-- Models
stg_<source>_<entity>      -- Staging: stg_raw_customers
int_<process>_<entity>     -- Intermediate: int_filtered_orders
mart_<area>_<entity>       -- Mart: mart_sales_summary
```

## Error Handling Patterns

```python
# File operations
def load_data_safe(filepath: str) -> pd.DataFrame:
    """Load data with error handling."""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"File is empty: {filepath}")
        return pd.DataFrame()

# API calls
def fetch_with_retry(url: str, retries: int = 3) -> dict:
    """Fetch data with retries."""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Visualization Preferences

### Standard Color Palettes

```python
# Use seaborn palettes
sns.set_palette('husl')        # Default
sns.set_palette('deep')        # Formal reports
sns.set_palette('colorblind')  # Accessibility
```

### Figure Sizes

```python
# Single plot
plt.figure(figsize=(12, 6))

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Publication quality
plt.figure(figsize=(10, 6), dpi=300)
```

### Plot Styling

```python
# Always add titles and labels
plt.title('Sales by Category', fontsize=14, fontweight='bold')
plt.xlabel('Category')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
```

## Dependencies & Versions

### Core Libraries (from requirements-datascience.txt)

- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- plotly >= 5.14.0
- dbt-core >= 1.5.0
- dbt-postgres >= 1.5.0

### Development Tools

- black (line-length: 88)
- flake8 (max-line-length: 88)
- isort (profile: black)
- pytest
- mypy

## AI Assistant Guidelines

When suggesting code for this workspace:

1. **Always use Path objects** from pathlib, not string paths
2. **Include type hints** for function parameters and returns
3. **Add docstrings** using Google style
4. **Use pandas vectorized operations** instead of loops
5. **Format with Black standards** (88 character lines)
6. **Handle errors gracefully** with try/except
7. **Validate data** before processing
8. **Add tests** for new functions
9. **Document assumptions** in comments
10. **Save intermediate results** for large computations

### For Jupyter Notebooks

- Add descriptive markdown cells explaining each section
- Include data validation checks
- Show data shapes and types
- Create clear visualizations with titles/labels
- Save important results to processed/

### For dbt Models

- Use CTEs for readability
- Add column-level documentation in .yml
- Include data quality tests
- Use ref() for dependencies
- Materialize large models as tables

### For Python Scripts

- Include if **name** == '**main**' blocks
- Use argparse for CLI arguments
- Log important operations
- Create reusable functions
- Handle file paths with Path objects

## Example Prompts That Work Well

"Create a dbt staging model for customer data with basic cleaning"
"Write a function to load and validate CSV data with error handling"
"Generate a Jupyter notebook for time series analysis"
"Create a visualization showing sales trends by category"
"Write tests for the data transformation function"
"Add documentation to this dbt model"

## Project-Specific Shortcuts

```python
# Quick data loading helper
def quick_load(filename: str) -> pd.DataFrame:
    """Quick load from raw data directory."""
    return pd.read_csv(Path.cwd().parent / 'data' / 'raw' / filename)

# Quick save helper
def quick_save(df: pd.DataFrame, filename: str) -> None:
    """Quick save to processed directory."""
    df.to_csv(Path.cwd().parent / 'data' / 'processed' / filename, index=False)
```

---

**Last Updated**: October 2025
**Maintained by**: Data Team
**Questions?**: See CONFIGURATION.md or DATA_SCIENCE_GUIDE.md
