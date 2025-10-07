# Scott County, Iowa - Cleaned Data Documentation

**Last Updated:** October 7, 2025  
**Data Source:** U.S. Census Bureau ACS 5-Year Estimates  
**Time Period:** 2009-2021  
**Geography:** Scott County, Iowa (State FIPS: 19, County FIPS: 163)

---

## 📁 Files Overview

### Unified Dataset (Recommended Starting Point)

**`scott_county_unified_timeseries.csv`** - Comprehensive time series dataset combining all key metrics

- **13 rows** (years 2009-2021)
- **17 columns** including demographics, income, education, employment, and housing
- **Best for:** Trend analysis, time series modeling, comparative analysis

### Historical Datasets (2009-2021 or subset)

1. **`scott_county_income_historical_cleaned.csv`**

   - Median household income, per capita income, poverty rates
   - 13 years of data (2009-2021)

2. **`scott_county_education_historical_cleaned.csv`**

   - Bachelor's degree attainment rates
   - 10 years of data (2012-2021)

3. **`scott_county_employment_historical_cleaned.csv`**

   - Civilian labor force, unemployment rates
   - 11 years of data (2011-2021)

4. **`scott_county_housing_historical_cleaned.csv`**

   - Median home values, median rent
   - 13 years of data (2009-2021)

5. **`scott_county_demographics_historical_cleaned.csv`**
   - Total population, median age, racial demographics
   - 13 years of data (2009-2021)

### 2021 Snapshot Datasets

Detailed 2021 data with many additional columns:

- `scott_county_income_2021_cleaned.csv` (32 columns)
- `scott_county_education_2021_cleaned.csv` (28 columns)
- `scott_county_employment_2021_cleaned.csv` (32 columns)
- `scott_county_housing_2021_cleaned.csv` (31 columns)
- `scott_county_demographics_2021_cleaned.csv` (52 columns)

### Data Dictionary

**`scott_county_data_dictionary.csv`** - Complete field documentation

- Column names and data types for all datasets
- Non-null counts and sample values
- Essential for understanding data structure

---

## 🔑 Key Columns in Unified Dataset

| Column                            | Description                           | Type    |
| --------------------------------- | ------------------------------------- | ------- |
| `year`                            | Year of observation (2009-2021)       | Integer |
| `geography_name`                  | "Scott County, Iowa"                  | String  |
| `state_fips`                      | State FIPS code (19 = Iowa)           | Integer |
| `county_fips`                     | County FIPS code (163 = Scott County) | Integer |
| `total_population`                | Total population estimate             | Integer |
| `median_age`                      | Median age in years                   | Float   |
| `median_household_income`         | Median household income ($)           | Integer |
| `per_capita_income`               | Per capita income ($)                 | Integer |
| `poverty_rate_pct`                | Percentage below poverty line         | Float   |
| `unemployment_rate_pct`           | Unemployment rate (%)                 | Float   |
| `bachelor's_degree_or_higher_pct` | % with bachelor's degree or higher    | Float   |
| `median_home_value`               | Median home value ($)                 | Integer |
| `median_gross_rent`               | Median monthly rent ($)               | Integer |

---

## 📊 Data Quality Summary

### Completeness

- ✅ **No duplicate rows** in any dataset
- ✅ **All datasets validated** successfully
- ✅ **Standardized column names** (snake_case format)
- ✅ **Consistent geography identifiers** across all datasets

### Coverage

- **Income:** Complete 13 years (2009-2021)
- **Housing:** Complete 13 years (2009-2021)
- **Demographics:** Complete 13 years (2009-2021)
- **Employment:** 11 years (2011-2021)
- **Education:** 10 years (2012-2021)

### Metadata Columns

All cleaned datasets include:

- `data_category` - Category of data (income, education, etc.)
- `data_type` - Either "historical" or "2021_snapshot"
- `processed_date` - Date the data was cleaned (2025-10-07)
- `state_name` - "Iowa"
- `county_name` - "Scott County"

---

## 📈 Key Insights from the Data

### Income Growth (2009-2021)

- **Start:** $50,656 (2009)
- **End:** $67,675 (2021)
- **Growth:** +$17,019 (+33.6%)
- **Annual Average:** +2.5% per year

### Population Trends

- Steady growth at approximately +931 people/year
- Represents about 5.5% of Iowa's total population

### Education Achievement

- Scott County: 43.5% bachelor's degree or higher (2021)
- Iowa State: 29.7% bachelor's degree or higher
- **Advantage:** +13.8 percentage points above state average

### Housing Market

- Median home value: $172,100 (2021)
- $11,400 (7.1%) higher than Iowa state average

---

## 🔧 Data Cleaning Operations Applied

1. **Column Name Standardization**

   - Converted to snake_case format
   - Removed special characters
   - Replaced % with 'pct'

2. **Geography Standardization**

   - Renamed 'NAME' to 'geography_name'
   - Renamed 'state' to 'state_fips'
   - Renamed 'county' to 'county_fips'
   - Added 'state_name' and 'county_name' columns

3. **Data Type Validation**

   - Converted numeric strings to proper numeric types
   - Ensured year columns are integers

4. **Metadata Addition**

   - Added processing metadata columns
   - Added geographic labels

5. **Sorting and Indexing**
   - Sorted historical data by year
   - Reset indices for clean row numbers

---

## 💡 Usage Examples

### Python (pandas)

```python
import pandas as pd
from pathlib import Path

# Load the unified time series dataset
data_dir = Path('c:/git/dbt/data/processed')
df = pd.read_csv(data_dir / 'scott_county_unified_timeseries.csv')

# Quick analysis
print(df[['year', 'median_household_income', 'unemployment_rate_pct']].tail())

# Calculate income growth
income_growth = df['median_household_income'].pct_change() * 100
df['income_growth_pct'] = income_growth

# Visualize trends
import matplotlib.pyplot as plt
df.plot(x='year', y='median_household_income', figsize=(12, 6))
plt.title('Scott County Income Trend')
plt.show()
```

### R

```r
library(tidyverse)

# Load data
df <- read_csv("c:/git/dbt/data/processed/scott_county_unified_timeseries.csv")

# View structure
glimpse(df)

# Calculate year-over-year changes
df <- df %>%
  arrange(year) %>%
  mutate(
    income_change = median_household_income - lag(median_household_income),
    income_change_pct = (income_change / lag(median_household_income)) * 100
  )

# Plot
ggplot(df, aes(x = year, y = median_household_income)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Scott County Median Household Income")
```

---

## 🎯 Recommended Analysis Paths

### 1. **Time Series Analysis**

- Trend analysis of income, education, housing over time
- Identify inflection points (e.g., 2020 income spike)
- Forecast future trends

### 2. **Comparative Analysis**

- Compare Scott County to Iowa state averages
- Benchmark against similar counties
- Identify competitive advantages

### 3. **Correlation Studies**

- Relationship between education and income
- Impact of unemployment on poverty rates
- Housing market trends vs. population growth

### 4. **Demographic Shifts**

- Population growth patterns
- Age distribution changes
- Racial/ethnic composition trends

### 5. **Economic Development**

- Income growth drivers
- Employment sector analysis
- Housing affordability trends

---

## 📚 Related Documentation

- **`SCOTT_COUNTY_ANALYSIS.md`** - Detailed analysis report
- **`scott_county_data_cleaning.ipynb`** - Complete cleaning workflow
- **`scott_county_data_dictionary.csv`** - Full data dictionary

---

## 🔄 Data Updates

This is historical data covering 2009-2021. For updated data:

1. Use the `scripts/fetch_data_gov.py` script to fetch new Census data
2. Run the `notebooks/scott_county_data_cleaning.ipynb` notebook
3. Data will be automatically cleaned and saved to this directory

---

## ⚠️ Important Notes

### Data Limitations

- **ACS 5-Year Estimates:** Data represents 5-year rolling averages
- **Margin of Error:** Census data includes sampling error (not included in these files)
- **Survey Changes:** Methodology may change slightly year-to-year
- **COVID-19 Impact:** 2020-2021 data may reflect pandemic effects

### Geographic Notes

- Data represents Scott County as a whole, not specific cities or townships
- County boundaries assumed stable over the time period
- Population estimates may differ from decennial census counts

### Citation

When using this data, please cite:

```
U.S. Census Bureau, American Community Survey 5-Year Estimates (2009-2021)
Processed and cleaned: October 7, 2025
```

---

## 🤝 Support

For questions or issues with this data:

1. Check the data dictionary for column definitions
2. Review the cleaning notebook for methodology
3. Consult the original SCOTT_COUNTY_ANALYSIS.md report

---

**Status:** ✅ Ready for Analysis  
**Quality:** Validated and cleaned  
**Format:** CSV (UTF-8)  
**Delimiter:** Comma  
**Missing Values:** Minimal (see data dictionary)
