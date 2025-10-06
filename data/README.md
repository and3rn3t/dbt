# Data Directory

This directory contains all data files for the project, organized by stage in the data pipeline.

## Directory Structure

```text
data/
├── raw/              # Original, immutable data dump
├── external/         # Data from third-party sources
├── staging/          # Intermediate transformed data
└── processed/        # Final, cleaned data ready for analysis
```

## Guidelines

### `/raw`

- **Purpose**: Store original, unmodified data files
- **Policy**: Never edit files in this directory
- **Examples**: Downloaded CSV files, API responses, database dumps
- **Note**: Large files are gitignored; keep only small sample files in version control

### `/external`

- **Purpose**: Data from external sources (APIs, web scraping, etc.)
- **Policy**: Keep metadata about data sources
- **Examples**: Data.gov datasets, public APIs, third-party data

### `/staging`

- **Purpose**: Intermediate processing steps
- **Policy**: Temporary storage for work-in-progress transformations
- **Examples**: Partially cleaned data, intermediate calculations

### `/processed`

- **Purpose**: Clean, validated data ready for analysis or modeling
- **Policy**: Well-documented, quality-checked data
- **Examples**: Feature-engineered datasets, aggregated metrics

## Data File Naming Convention

Use descriptive names with dates:

- `YYYY-MM-DD_source_description.csv`
- Example: `2024-01-15_sales_transactions_cleaned.csv`

## Large Files

For files > 50MB:

1. Add to `.gitignore`
2. Document location in `data/SOURCES.md`
3. Consider using Git LFS or cloud storage
4. Provide download/generation scripts

## Data Documentation

Each subdirectory should contain:

- `README.md` - Description of data sources
- `SOURCES.md` - Links and references to original data
- `schema.md` - Data dictionary and column descriptions
