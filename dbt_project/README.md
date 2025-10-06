# dbt Project

Data transformation and modeling using dbt (data build tool).

## Setup

1. Install dbt: `pip install dbt-core dbt-postgres`
2. Configure your database credentials in `.env`
3. Copy `profiles.yml` to `~/.dbt/` or set `DBT_PROFILES_DIR` environment variable

## Project Structure

```
dbt_project/
├── models/
│   ├── staging/     # Raw data cleaning and standardization
│   └── marts/       # Business logic and aggregations
├── seeds/           # CSV files to load into database
├── tests/           # Custom data tests
└── dbt_project.yml  # Configuration file
```

## Common Commands

```bash
# Install dependencies
dbt deps

# Run all models
dbt run

# Run specific model
dbt run --select model_name

# Test data quality
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

## Model Naming Conventions

- **Staging**: `stg_<source>_<entity>.sql`
- **Marts**: `mart_<area>_<entity>.sql`

## Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [Best Practices](https://docs.getdbt.com/guides/best-practices)
