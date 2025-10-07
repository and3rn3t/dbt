# US Census Bureau Education Data - Quick Start Guide

## 🎯 What You're Getting

The **American Community Survey (ACS)** from the US Census Bureau provides the most comprehensive education data available:

- **Educational Attainment** by geographic area (25 years and over)
- **Most Recent Data**: 2021 ACS 5-Year Estimates (2017-2021 data)
- **Geography Levels**: National, State, County, Census Tract
- **25 Education Categories**: From "No schooling" to "Doctorate degree"

---

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your Free API Key (2 minutes)

1. Visit: https://api.census.gov/data/key_signup.html
2. Fill in your name and email
3. Check your email (key arrives instantly)
4. Add to your `.env` file:
   ```bash
   CENSUS_API_KEY=your_key_here_from_email
   ```

### Step 2: Fetch Data

```powershell
# All states education data (most popular)
python scripts/fetch_census_education.py --geography state --preview

# California counties only
python scripts/fetch_census_education.py --geography county --state 06 --preview

# National summary
python scripts/fetch_census_education.py --geography us --preview
```

### Step 3: Analyze in Jupyter

```powershell
jupyter lab
# Open the saved CSV file from data/raw/
```

---

## 📊 Available Data

### Education Categories (Detailed Mode)

When you use `--detailed`, you get 25 education levels:

1. **Elementary**: Grades 1-8
2. **High School**: Grades 9-12 (with/without diploma)
3. **Some College**: Less than 1 year, 1+ years
4. **Associate's Degree**
5. **Bachelor's Degree**
6. **Master's Degree**
7. **Professional Degree** (Law, Medicine, etc.)
8. **Doctorate Degree**

### Education Categories (Summary Mode - Default)

The default mode provides 14 key indicators by gender:

- High school graduates
- Some college or associate's degree
- Bachelor's degree
- Master's degree
- Professional school degree
- Doctorate degree

---

## 🗺️ Geography Options

### 1. National Level (--geography us)

```powershell
python scripts/fetch_census_education.py --geography us
```

**Returns**: 1 row with US totals
**Best for**: National overview, baseline comparisons

### 2. State Level (--geography state)

```powershell
python scripts/fetch_census_education.py --geography state
```

**Returns**: 52 rows (50 states + DC + Puerto Rico)
**Best for**: State comparisons, rankings, regional patterns

### 3. County Level (--geography county)

```powershell
python scripts/fetch_census_education.py --geography county --state 06
```

**Returns**: All counties in specified state
**Best for**: Detailed state analysis, urban vs rural

### 4. Census Tract Level (--geography tract)

```powershell
python scripts/fetch_census_education.py --geography tract --state 36
```

**Returns**: All census tracts in state (can be 1000+)
**Best for**: Neighborhood analysis, very granular patterns

---

## 🔢 Common State FIPS Codes

| Code | State      | Code | State     | Code | State          |
| ---- | ---------- | ---- | --------- | ---- | -------------- |
| 06   | California | 36   | New York  | 48   | Texas          |
| 12   | Florida    | 17   | Illinois  | 42   | Pennsylvania   |
| 13   | Georgia    | 39   | Ohio      | 53   | Washington     |
| 04   | Arizona    | 26   | Michigan  | 37   | North Carolina |
| 51   | Virginia   | 27   | Minnesota | 24   | Maryland       |

Full list: https://www.census.gov/library/reference/code-lists/ansi.html

---

## 📋 Real Examples

### Example 1: Compare All States

```powershell
# Fetch all states with detailed breakdown
python scripts/fetch_census_education.py --geography state --detailed --preview
```

**What you get:**

- Educational attainment for all 50 states
- Percentages automatically calculated
- "Bachelor's degree or higher" aggregate metric
- Ready for ranking and visualization

**Analysis ideas:**

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/raw/census_education_2021_state_*.csv')

# Top 10 states by bachelor's degree or higher
top_10 = df.nlargest(10, "Bachelor's degree or higher (%)")
top_10[['NAME', "Bachelor's degree or higher (%)"]].plot(kind='barh')
plt.title('Top 10 States by College Degree Attainment')
plt.show()
```

---

### Example 2: California Deep Dive

```powershell
# Get all California counties
python scripts/fetch_census_education.py --geography county --state 06 --preview
```

**What you get:**

- 58 California counties
- Education levels for each
- Urban vs rural patterns visible

**Analysis ideas:**

```python
# Compare Bay Area counties
bay_area = ['San Francisco', 'Santa Clara', 'Alameda', 'San Mateo']
bay_df = df[df['NAME'].str.contains('|'.join(bay_area))]

# Plot bachelor's degree rates
bay_df.plot(x='NAME', y="Bachelor's degree or higher (%)", kind='bar')
```

---

### Example 3: Multi-State Comparison

```powershell
# Fetch multiple states and combine
python scripts/fetch_census_education.py --geography county --state 06
python scripts/fetch_census_education.py --geography county --state 36
python scripts/fetch_census_education.py --geography county --state 48
```

**Combine in Python:**

```python
import pandas as pd
from pathlib import Path

# Load all county files
county_files = Path('data/raw').glob('census_education_*_county_*.csv')
df_list = [pd.read_csv(f) for f in county_files]
all_counties = pd.concat(df_list, ignore_index=True)

# Now analyze cross-state patterns
```

---

## 🎨 Visualization Ideas

### 1. State Heatmap

```python
import plotly.express as px

fig = px.choropleth(
    df,
    locations='state',
    locationmode='USA-states',
    color="Bachelor's degree or higher (%)",
    scope='usa',
    title='College Education by State'
)
fig.show()
```

### 2. Education Pyramid

```python
import matplotlib.pyplot as plt

education_levels = ['No schooling', 'High school', "Bachelor's", "Master's", 'Doctorate']
values = [df[level].sum() for level in education_levels]

plt.barh(education_levels, values)
plt.title('Educational Attainment Distribution')
plt.xlabel('Population (25+ years)')
plt.show()
```

### 3. Correlation Analysis

```python
# Merge with economic data
import pandas as pd

education_df = pd.read_csv('census_education.csv')
income_df = pd.read_csv('census_income.csv')

merged = education_df.merge(income_df, on='state')
merged.plot.scatter(x="Bachelor's degree or higher (%)", y='Median Income')
```

---

## 💡 Pro Tips

### 1. Start Small

```powershell
# Start with national/state level before going to county/tract
python scripts/fetch_census_education.py --geography state
```

### 2. Use Preview Mode

```powershell
# Always use --preview first to see what you're getting
python scripts/fetch_census_education.py --geography state --preview
```

### 3. Detailed vs Summary

```powershell
# Summary (default) is usually enough
python scripts/fetch_census_education.py --geography state

# Only use --detailed if you need all 25 categories
python scripts/fetch_census_education.py --geography state --detailed
```

### 4. Combine with Other Census Data

The Census API has many datasets you can fetch similarly:

- **Income**: Replace education variables with income variables
- **Race/Ethnicity**: Use demographic tables
- **Housing**: Home ownership, costs, etc.
- **Poverty**: Poverty rates by area

---

## 📊 Sample Output

After running:

```powershell
python scripts/fetch_census_education.py --geography state --preview
```

You'll see:

```
================================================================================
FETCHING CENSUS EDUCATION DATA
================================================================================
Dataset: American Community Survey (ACS) 2021 5-Year Estimates
Geography: All States
Variables: 14 education indicators
Detail Level: Summary (14 categories)
================================================================================

Downloading data from Census Bureau API...
✓ Downloaded 52 geographic areas
✓ Columns: 28

Calculating education metrics...
✓ Calculated percentage distributions
✓ Created aggregate education categories

Saving data...
✓ Saved to: data/raw/census_education_2021_state_20251006_220000.csv
✓ Records: 52
✓ Size: 0.03 MB

================================================================================
DATA PREVIEW (first 5 rows)
================================================================================

                NAME  Total population 25 years and over  Male: High school graduate  ...
0      United States                           222168275                     25897884  ...
1            Alabama                             3378351                       435199  ...
2             Alaska                              504492                        56125  ...
3            Arizona                             4896849                       531009  ...
4           Arkansas                             2064266                       266398  ...
```

---

## 🎯 What to Do Next

1. **Get API Key** (2 minutes): https://api.census.gov/data/key_signup.html
2. **Fetch State Data**: `python scripts/fetch_census_education.py --geography state --preview`
3. **Open in Jupyter**: Analyze, visualize, and explore patterns
4. **Combine with NYC Education**: Compare federal vs local data
5. **Create Dashboard**: Add to your Streamlit dashboard

---

## 🆘 Troubleshooting

### "CENSUS API KEY REQUIRED"

→ Get free key: https://api.census.gov/data/key_signup.html
→ Add to `.env`: `CENSUS_API_KEY=your_key`

### "Error: --state required for county geography"

→ Add state FIPS code: `--state 06` for California

### Connection timeout

→ Census API can be slow; try smaller geography first
→ Add `timeout=60` if needed

### No data returned

→ Check FIPS code is valid
→ Try different year (2021, 2020, 2019)

---

## 📚 Resources

- **Census API Docs**: https://www.census.gov/data/developers/data-sets/acs-5year.html
- **Variable List**: https://api.census.gov/data/2021/acs/acs5/variables.html
- **Geography Info**: https://www.census.gov/programs-surveys/geography.html
- **FIPS Codes**: https://www.census.gov/library/reference/code-lists/ansi.html

---

## ✅ Ready to Start!

Run this command to get your first Census education dataset:

```powershell
python scripts/fetch_census_education.py --geography state --preview
```

Then explore the data in Jupyter Lab! 🚀
