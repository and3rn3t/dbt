# GitHub Copilot Instructions

This file provides context to GitHub Copilot about the project structure, conventions, and best practices.

## Project Overview

This is a **data science and analytics workspace** that combines:
- **Data analysis** using Python, Pandas, NumPy, and Jupyter notebooks
- **Data transformation** using dbt (data build tool)
- **Data visualization** with Matplotlib, Seaborn, and Plotly
- **Machine learning** capabilities (scikit-learn, TensorFlow, PyTorch available)

## Tech Stack

### Core Technologies
- **Python 3.11+** - Primary programming language
- **dbt** - Data transformation and modeling
- **Jupyter** - Interactive notebooks for analysis
- **PostgreSQL** - Database (via dbt-postgres)
- **Docker** - Containerization (optional)

### Data Science Libraries
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib, seaborn, plotly** - Visualization
- **scipy** - Scientific computing
- **scikit-learn** - Machine learning (when needed)

### Development Tools
- **black** - Code formatting (line length: 88)
- **isort** - Import sorting
- **flake8** - Linting
- **pytest** - Testing
- **mypy** - Type checking

## Project Structure

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
│   └── fetch_data_gov.py         # Data fetching utilities
├── dbt_project/                  # dbt models and configuration
│   ├── models/                   # SQL transformation models
│   │   ├── staging/              # Staging layer models
│   │   └── marts/                # Business logic layer
│   ├── seeds/                    # CSV files to load
│   └── dbt_project.yml           # dbt configuration
├── templates/                     # Code templates
├── tests/                        # Test files
└── docs/                         # Documentation

## Coding Standards & Conventions

### Python Code Style

1. **Formatting**: Use Black (line length: 88 characters)
   ```python
   # Good
   def process_data(df: pd.DataFrame) -> pd.DataFrame:
       """Process and clean the dataframe."""
       return df.dropna().reset_index(drop=True)
   ```

2. **Imports**: Use isort for organizing imports
   ```python
   # Standard library
   import os
   from pathlib import Path
   
   # Third-party
   import pandas as pd
   import numpy as np
   
   # Local
   from scripts import utils
   ```

3. **Type Hints**: Use type hints for function signatures
   ```python
   def calculate_metrics(data: pd.DataFrame, column: str) -> dict[str, float]:
       return {"mean": data[column].mean(), "std": data[column].std()}
   ```

4. **Docstrings**: Use Google-style docstrings
   ```python
   def load_data(filepath: str) -> pd.DataFrame:
       """Load data from CSV file.
       
       Args:
           filepath: Path to the CSV file
           
       Returns:
           DataFrame with loaded data
           
       Raises:
           FileNotFoundError: If file doesn't exist
       """
       return pd.read_csv(filepath)
   ```

### SQL (dbt) Style

1. **Naming**: Use snake_case for models and columns
   ```sql
   -- staging models: stg_<source>_<entity>.sql
   -- marts models: mart_<area>_<entity>.sql
   ```

2. **Structure**: Use CTEs for readability
   ```sql
   with source_data as (
       select * from {{ source('raw', 'table_name') }}
   ),
   
   transformed as (
       select
           id,
           lower(name) as name,
           created_at
       from source_data
   )
   
   select * from transformed
   ```

3. **Formatting**: Lowercase keywords, one column per line
   ```sql
   select
       customer_id,
       order_date,
       total_amount
   from orders
   where status = 'completed'
   ```

### File Naming Conventions

- **Python scripts**: `snake_case.py` (e.g., `fetch_data_gov.py`)
- **Notebooks**: `descriptive_name.ipynb` (e.g., `customer_analysis.ipynb`)
- **dbt staging**: `stg_<source>_<entity>.sql` (e.g., `stg_raw_customers.sql`)
- **dbt marts**: `mart_<area>_<entity>.sql` (e.g., `mart_sales_summary.sql`)
- **Data files**: `YYYY-MM-DD_source_description.csv`

## Common Patterns & Examples

### Data Loading Pattern

```python
from pathlib import Path
import pandas as pd

# Use Path for cross-platform compatibility
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

def load_raw_data(filename: str) -> pd.DataFrame:
    """Load data from raw directory."""
    filepath = DATA_DIR / 'raw' / filename
    return pd.read_csv(filepath)

def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    """Save processed data."""
    filepath = DATA_DIR / 'processed' / filename
    df.to_csv(filepath, index=False)
```

### Notebook Structure Pattern

```python
# 1. Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 2. Configuration
%matplotlib inline
pd.set_option('display.max_columns', None)
sns.set_style('whitegrid')

# 3. Load data
PROJECT_ROOT = Path.cwd().parent
data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'data.csv')

# 4. Explore and analyze
print(data.info())
print(data.describe())

# 5. Visualize
fig, ax = plt.subplots(figsize=(12, 6))
data['column'].hist(ax=ax)
plt.show()

# 6. Save results
data.to_csv(PROJECT_ROOT / 'data' / 'processed' / 'cleaned.csv', index=False)
```

### dbt Model Pattern

```sql
-- models/staging/stg_source_entity.sql
{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'source_table') }}
),

renamed as (
    select
        id as entity_id,
        name as entity_name,
        created_at,
        updated_at
    from source
    where deleted_at is null
)

select * from renamed
```

## Environment & Configuration

### Environment Variables

Never hardcode credentials. Use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
API_KEY = os.getenv('API_KEY')
```

### Path Handling

Always use `pathlib.Path` for cross-platform compatibility:

```python
from pathlib import Path

# Good
data_path = Path('data') / 'raw' / 'file.csv'

# Avoid
data_path = 'data/raw/file.csv'  # Won't work on Windows
```

## Data Handling Best Practices

### 1. Data Validation

```python
def validate_dataframe(df: pd.DataFrame) -> None:
    """Validate dataframe meets expectations."""
    assert not df.empty, "DataFrame is empty"
    assert df['id'].is_unique, "IDs must be unique"
    assert df['amount'].notna().all(), "Amount cannot be null"
```

### 2. Missing Data

```python
# Check for missing data
print(df.isnull().sum())

# Handle missing data appropriately
df_clean = df.dropna(subset=['critical_column'])
df_filled = df.fillna({'optional_column': 0})
```

### 3. Data Types

```python
# Ensure correct data types
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].astype('category')
df['amount'] = df['amount'].astype(float)
```

### 4. Memory Optimization

```python
# For large datasets, use appropriate dtypes
df = pd.read_csv(
    'large_file.csv',
    dtype={'id': 'int32', 'category': 'category'},
    parse_dates=['date']
)
```

## Testing Guidelines

### Unit Tests

```python
import pytest
import pandas as pd
from scripts.utils import clean_data

def test_clean_data_removes_nulls():
    """Test that clean_data removes null values."""
    df = pd.DataFrame({'a': [1, None, 3], 'b': [4, 5, 6]})
    result = clean_data(df)
    assert result['a'].notna().all()

def test_clean_data_preserves_columns():
    """Test that clean_data preserves column names."""
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    result = clean_data(df)
    assert list(result.columns) == ['a', 'b']
```

### dbt Tests

```yaml
# models/staging/staging.yml
models:
  - name: stg_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
          - not_null
```

## Security & Privacy

### ⚠️ Never commit:
- API keys, passwords, tokens
- Database credentials
- Personal identifiable information (PII)
- Large data files (>50MB)
- `.env` files with actual values

### ✅ Always:
- Use `.env` for secrets
- Add sensitive files to `.gitignore`
- Anonymize data before analysis
- Use `.env.example` as template

## Documentation Guidelines

### Code Comments

```python
# Good: Explain WHY, not WHAT
# Calculate weighted average to account for sample size differences
weighted_avg = (df['value'] * df['weight']).sum() / df['weight'].sum()

# Avoid: Obvious comments
# Calculate sum
total = df['value'].sum()
```

### Notebook Markdown Cells

```markdown
## Data Loading and Exploration

Load the customer transaction data and perform initial exploration:
- Check data quality
- Identify missing values
- Understand distributions

Key findings:
- 1,000 transactions from Jan-Dec 2024
- 5% missing values in amount column
- Average transaction: $254.50
```

## Performance Tips

### Pandas Optimization

```python
# Use vectorized operations instead of loops
# Good
df['total'] = df['quantity'] * df['price']

# Avoid
df['total'] = df.apply(lambda row: row['quantity'] * row['price'], axis=1)

# Use query for filtering
filtered = df.query('amount > 100 and status == "active"')

# Use categorical for repeated strings
df['category'] = df['category'].astype('category')
```

### Memory Management

```python
# Read large files in chunks
chunks = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in chunks:
    process(chunk)

# Use appropriate dtypes
df = df.astype({'id': 'int32', 'value': 'float32'})
```

## Troubleshooting Common Issues

### Import Errors
```python
# Ensure PYTHONPATH is set correctly
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
```

### Jupyter Kernel Issues
```bash
# Reinstall kernel
pip install ipykernel
python -m ipykernel install --user
```

### dbt Issues
```bash
# Clean and rebuild
dbt clean
dbt deps
dbt run
```

## Additional Context

- **Data Sources**: Document in `data/SOURCES.md`
- **Model Documentation**: Create `.yml` files alongside SQL files
- **Analysis Results**: Save in `notebooks/` with clear names
- **Reusable Code**: Extract to `scripts/` directory

## Quick Commands

```bash
# Format code
black . && isort .

# Lint
flake8 .

# Test
pytest

# Run dbt
dbt run
dbt test

# Start Jupyter
jupyter lab
```

---

## Copilot-Specific Hints

When suggesting code:
1. Prefer pandas vectorized operations over loops
2. Use type hints for function parameters
3. Include error handling for file operations
4. Add docstrings to functions
5. Use Path objects for file paths
6. Follow Black formatting (88 char line length)
7. Include data validation checks
8. Add comments for complex logic
9. Suggest appropriate visualizations
10. Consider memory efficiency for large datasets

When working with notebooks:
- Add descriptive markdown cells
- Clear outputs before suggesting cell edits
- Include visualization titles and labels
- Save important results to files
- Document data sources and assumptions

When working with SQL/dbt:
- Use CTEs for readability
- Add tests for data quality
- Document models in .yml files
- Use ref() for model dependencies
- Use source() for raw tables
