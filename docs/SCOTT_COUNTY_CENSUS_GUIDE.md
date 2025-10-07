# Scott County, Iowa - Census Data Guide

## 📍 Location Information

- **County**: Scott County
- **State**: Iowa
- **State FIPS**: 19
- **County FIPS**: 163
- **Major Cities**: Davenport, Bettendorf, Eldridge, LeClaire
- **Population**: ~172,000 (2020)

---

## 🎯 What Data You're Getting

This comprehensive Census data pull includes **5 major datasets** for Scott County:

### 1. 📚 Educational Attainment

- Total population 25 years and over
- Education levels from "No schooling" to "Doctorate degree"
- High school graduate rates
- College degree attainment (Associate's, Bachelor's, Master's, Professional, Doctorate)
- **Auto-calculated**: Bachelor's degree or higher percentage

### 2. 💰 Income and Poverty

- Median household income
- Per capita income
- Aggregate household income
- Household income distribution (17 income brackets from <$10k to $200k+)
- Poverty population and rates
- **Auto-calculated**: Poverty rate percentage

### 3. 👥 Demographics (Age, Race, Ethnicity)

- Total population
- Median age
- Age distribution by gender (25 age groups)
- Race categories (White, Black, Asian, Native American, Pacific Islander, Other, Two or more)
- Hispanic/Latino origin
- **Auto-calculated**: Percentage distributions for all race categories

### 4. 🏠 Housing Characteristics

- Total housing units
- Occupied vs vacant units
- Owner occupied vs renter occupied
- Median home value
- Median gross rent
- Units in structure (single-family, multi-family, mobile homes)
- **Auto-calculated**: Homeownership rate, vacancy rate

### 5. 💼 Employment and Industry

- Labor force population (16+ years)
- Employment status (employed, unemployed, not in labor force)
- Industry breakdown (13 major industries):
  - Agriculture, forestry, fishing, hunting, mining
  - Construction
  - Manufacturing
  - Wholesale trade
  - Retail trade
  - Transportation, warehousing, utilities
  - Information
  - Finance, insurance, real estate
  - Professional, scientific, management
  - Educational services, health care, social assistance
  - Arts, entertainment, recreation, accommodation, food services
  - Other services
  - Public administration
- **Auto-calculated**: Unemployment rate, labor force participation rate

---

## 🚀 Quick Start

### Step 1: Get Census API Key (2 minutes)

1. Visit: **<https://api.census.gov/data/key_signup.html>**
2. Enter name and email
3. Check email for instant key
4. Add to `.env` file:

   ```
   CENSUS_API_KEY=your_key_from_email
   ```

### Step 2: Fetch All Data

```powershell
# Fetch all 5 datasets for Scott County, Iowa
python scripts/fetch_scott_county_census.py
```

This will:

- ✅ Fetch all 5 Census datasets
- ✅ Calculate percentages and metrics automatically
- ✅ Save 5 CSV files to `data/raw/`
- ✅ Display comprehensive summary report
- ✅ Show key statistics for the county

**Output files:**

- `scott_county_iowa_education_2021_*.csv`
- `scott_county_iowa_income_2021_*.csv`
- `scott_county_iowa_demographics_2021_*.csv`
- `scott_county_iowa_housing_2021_*.csv`
- `scott_county_iowa_employment_2021_*.csv`

---

## 📋 Advanced Options

### Fetch Specific Dataset Only

```powershell
# Just education data
python scripts/fetch_scott_county_census.py --dataset education

# Just income data
python scripts/fetch_scott_county_census.py --dataset income

# Just demographics
python scripts/fetch_scott_county_census.py --dataset demographics
```

### Use Different Year

```powershell
# Get 2020 data instead of 2021
python scripts/fetch_scott_county_census.py --year 2020

# Get 2019 data
python scripts/fetch_scott_county_census.py --year 2019
```

---

## 📊 Sample Output

When you run the script, you'll see:

```
================================================================================
FETCHING CENSUS DATA FOR Scott County, Iowa
================================================================================
State FIPS: 19 (Iowa)
County FIPS: 163 (Scott County)
Year: 2021 ACS 5-Year Estimates
================================================================================

================================================================================
Fetching: Educational Attainment
================================================================================
Location: Scott County, Iowa
Variables: 9
Year: 2021 ACS 5-Year Estimates
Downloading...
✓ Downloaded 9 indicators
✓ Saved: scott_county_iowa_education_2021_20251006_210730.csv
✓ Size: 2.45 KB

[... similar output for income, demographics, housing, employment ...]

================================================================================
SCOTT COUNTY, IOWA - CENSUS DATA SUMMARY (2021)
================================================================================

📊 Educational Attainment
--------------------------------------------------------------------------------
   College educated (bachelor's+): 32.5%
   High school graduates: 45,678

📊 Income and Poverty
--------------------------------------------------------------------------------
   Median household income: $67,543
   Per capita income: $34,567
   Poverty rate: 10.2%

📊 Age, Race, and Ethnicity
--------------------------------------------------------------------------------
   Total population: 172,943
   Median age: 38.5 years
   White: 83.4%
   Hispanic or Latino: 6.8%

📊 Housing Characteristics
--------------------------------------------------------------------------------
   Total housing units: 72,145
   Homeownership rate: 67.8%
   Median home value: $189,400
   Median rent: $875

📊 Employment and Industry
--------------------------------------------------------------------------------
   Unemployment rate: 3.2%
   Labor force participation: 68.5%
   Total employed: 87,234

================================================================================
```

---

## 🎨 Analysis Ideas

### 1. Compare Scott County to Iowa State Average

```python
import pandas as pd

# Load Scott County data
scott_education = pd.read_csv('data/raw/scott_county_iowa_education_2021_*.csv')

# Fetch Iowa state data
# python scripts/fetch_census_education.py --geography state --state 19

# Compare
print(f"Scott County Bachelor's+: {scott_education['Bachelor\'s degree or higher (%)'].iloc[0]:.1f}%")
print(f"Iowa State Bachelor's+: {iowa_education['Bachelor\'s degree or higher (%)'].iloc[0]:.1f}%")
```

### 2. Income Distribution Visualization

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data/raw/scott_county_iowa_income_2021_*.csv')

# Extract income brackets
income_brackets = [col for col in df.columns if 'Households with income' in col]
values = df[income_brackets].iloc[0].values

plt.figure(figsize=(12, 6))
plt.bar(range(len(income_brackets)), values)
plt.title('Scott County, Iowa - Household Income Distribution')
plt.xlabel('Income Bracket')
plt.ylabel('Number of Households')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### 3. Employment by Industry

```python
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/raw/scott_county_iowa_employment_2021_*.csv')

# Get industry columns
industry_cols = [col for col in df.columns if col not in ['NAME', 'state', 'county', 'Total employed', 'Population 16 years and over']]

# Create pie chart
fig = px.pie(
    values=df[industry_cols].iloc[0].values,
    names=industry_cols,
    title='Scott County, Iowa - Employment by Industry'
)
fig.show()
```

### 4. Age Pyramid

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/raw/scott_county_iowa_demographics_2021_*.csv')

# Get male age groups (would need to add female columns too)
male_cols = [col for col in df.columns if col.startswith('Male:')]
ages = df[male_cols].iloc[0].values

plt.barh(range(len(male_cols)), ages)
plt.title('Scott County, Iowa - Age Distribution (Male)')
plt.xlabel('Population')
plt.ylabel('Age Group')
plt.show()
```

---

## 🔗 Combine with Other Data

### Link to NYC Education Data

```python
# Compare Scott County to NYC boroughs
scott_df = pd.read_csv('data/raw/scott_county_iowa_education_2021_*.csv')
nyc_df = pd.read_csv('data/raw/nyc_sat_scores_*.csv')

# Analysis: Urban vs rural education patterns
```

### Add Economic Indicators

```python
# Fetch BLS unemployment data for Scott County
# Combine with Census employment data
# Analyze trends over time
```

---

## 📚 Data Dictionary

### Key Variables Explained

**Education:**

- `B15003_001E`: Total population 25+ (denominator for education rates)
- `B15003_021E`: Bachelor's degree holders
- `B15003_022E`: Master's degree holders

**Income:**

- `B19013_001E`: Median household income (middle point of all households)
- `B19301_001E`: Per capita income (total income / population)
- `B17001_002E`: Population below poverty line

**Demographics:**

- `B01001_001E`: Total population count
- `B01002_001E`: Median age
- `B02001_002E`: White alone population

**Housing:**

- `B25077_001E`: Median home value for owner-occupied units
- `B25064_001E`: Median monthly gross rent

**Employment:**

- `B23025_004E`: Employed population
- `B23025_005E`: Unemployed population

---

## 🎯 Next Steps After Fetching

1. **Load in Jupyter Lab**

   ```powershell
   jupyter lab
   ```

2. **Create Combined Dataset**

   ```python
   import pandas as pd
   from pathlib import Path

   # Load all datasets
   files = Path('data/raw').glob('scott_county_iowa_*_2021_*.csv')
   dfs = {f.stem.split('_')[3]: pd.read_csv(f) for f in files}

   # Combine into single wide dataset
   combined = pd.concat(dfs.values(), axis=1)
   combined.to_csv('data/processed/scott_county_complete.csv', index=False)
   ```

3. **Create Dashboard**

   - Add Scott County data to your Streamlit dashboard
   - Create comparison views (urban vs rural)
   - Show demographic trends

4. **Export Report**
   - Generate PDF report with key statistics
   - Create infographic with Plotly
   - Share insights with stakeholders

---

## ✅ Benefits of This Data

- ✅ **Comprehensive**: 5 major Census datasets in one pull
- ✅ **Automatic Calculations**: Percentages and rates computed for you
- ✅ **Clean Format**: Ready-to-analyze CSV files
- ✅ **Summary Report**: Instant overview of key metrics
- ✅ **Flexible**: Fetch all at once or one dataset at a time
- ✅ **Up-to-date**: Uses most recent ACS 5-Year Estimates (2021)
- ✅ **Comparable**: Same structure as state/national data for easy comparison

---

## 🆘 Troubleshooting

### "CENSUS API KEY REQUIRED"

→ Get free key: <https://api.census.gov/data/key_signup.html>  
→ Add to .env: `CENSUS_API_KEY=your_key`

### Connection Issues

→ Census API can be slow, be patient  
→ Try one dataset at a time: `--dataset education`

### Missing Data

→ Some variables may be null (data suppressed for privacy)  
→ Check Census documentation for variable definitions

---

## 📖 Resources

- **Census API**: <https://www.census.gov/data/developers/data-sets/acs-5year.html>
- **Scott County Info**: <https://www.scottcountyiowa.gov/>
- **Variable Definitions**: <https://api.census.gov/data/2021/acs/acs5/variables.html>
- **Geography Reference**: <https://www.census.gov/geographies.html>

---

## 🚀 Ready to Fetch

Run this command to get all Census data for Scott County, Iowa:

```powershell
python scripts/fetch_scott_county_census.py
```

Then explore in Jupyter Lab! 📊
