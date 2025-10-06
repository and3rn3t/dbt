# 🎓 NYC Education Data - Analysis Guide

## ✅ What We Just Fetched

You now have **2 comprehensive NYC education datasets**:

### 1. SAT Scores by School (zt9s-n5aj)

- **File**: `zt9s-n5aj_20251006_114228.csv`
- **Records**: 460 NYC high schools
- **Size**: 25 KB
- **Columns**: 6
  - School name and DBN code
  - Number of test takers
  - Math, Reading, Writing mean scores

**Key Insights:**

- Average Total SAT: **1,215**
- Top School: **Stuyvesant High School (2,087)**
- Score Range: 914 - 2,087

### 2. School Demographics (s3k6-pzi2)

- **File**: `s3k6-pzi2_20251006_114239.csv`
- **Records**: 440 schools
- **Size**: 1.4 MB
- **Columns**: 343 (very comprehensive!)
  - School information (name, DBN, borough)
  - Academic programs and opportunities
  - Enrollment details
  - Program offerings

**Borough Distribution:**

- Brooklyn (K): 124 schools
- Bronx (X): 118 schools
- Manhattan (M): 108 schools
- Queens (Q): 80 schools
- Staten Island (R): 10 schools

---

## 📊 Your Complete Data Collection

| Dataset                     | Records   | Size       | Category      | Source            |
| --------------------------- | --------- | ---------- | ------------- | ----------------- |
| **NYC SAT Scores**          | 460       | 25 KB      | Education     | NYC Open Data     |
| **NYC School Demographics** | 440       | 1.4 MB     | Education     | NYC Open Data     |
| Seattle Police Reports      | 6,650     | 1.1 MB     | Public Safety | Seattle Open Data |
| NYC 311 Requests            | 1,000     | 163 KB     | Government    | NYC Open Data     |
| Sample Sales Data           | 1,000     | 55 KB      | Business      | Sample            |
| **TOTAL**                   | **9,550** | **2.7 MB** | Multiple      | Multiple          |

---

## 🎯 Analysis Ideas

### Quick Wins (15 minutes)

#### 1. Top Performing Schools

```python
from scripts.utils import load_csv
import pandas as pd

# Load SAT data
sat = load_csv("zt9s-n5aj_20251006_114228.csv")

# Convert to numeric
for col in ['mathematics_mean', 'critical_reading_mean', 'writing_mean']:
    sat[col] = pd.to_numeric(sat[col], errors='coerce')

# Calculate total scores
sat['total_score'] = (sat['mathematics_mean'] +
                      sat['critical_reading_mean'] +
                      sat['writing_mean'])

# Top 10 schools
top_10 = sat.nlargest(10, 'total_score')[['school_name', 'total_score']]
print(top_10)
```

#### 2. Score Distribution by Borough

```python
from scripts.utils import load_csv
import pandas as pd
import matplotlib.pyplot as plt

# Load both datasets
sat = load_csv("zt9s-n5aj_20251006_114228.csv")
demo = load_csv("s3k6-pzi2_20251006_114239.csv")

# Merge on DBN (school code)
merged = sat.merge(demo[['dbn', 'boro']], on='dbn', how='left')

# Convert scores to numeric
merged['mathematics_mean'] = pd.to_numeric(merged['mathematics_mean'], errors='coerce')

# Group by borough
borough_scores = merged.groupby('boro')['mathematics_mean'].mean().sort_values(ascending=False)

# Visualize
borough_scores.plot(kind='bar', title='Average SAT Math Score by Borough')
plt.ylabel('Average Math Score')
plt.show()
```

#### 3. Test Participation Analysis

```python
from scripts.utils import load_csv
import pandas as pd

sat = load_csv("zt9s-n5aj_20251006_114228.csv")

# Convert to numeric
sat['number_of_test_takers'] = pd.to_numeric(sat['number_of_test_takers'], errors='coerce')

# Summary statistics
print(f"Average test takers per school: {sat['number_of_test_takers'].mean():.0f}")
print(f"Median: {sat['number_of_test_takers'].median():.0f}")
print(f"Max: {sat['number_of_test_takers'].max():.0f}")

# Schools with most test takers
top_participation = sat.nlargest(5, 'number_of_test_takers')[['school_name', 'number_of_test_takers']]
print("\nTop 5 schools by test participation:")
print(top_participation)
```

### Deep Analysis (1-2 hours)

#### 1. Correlation Analysis

Analyze the relationship between:

- School size (from demographics) vs SAT scores
- Borough location vs performance
- Program offerings vs outcomes

#### 2. Performance Gaps

- Identify schools that over/underperform expectations
- Compare specialized schools vs regular schools
- Analyze score distributions within boroughs

#### 3. Predictive Modeling

Build models to predict:

- SAT scores based on school characteristics
- Which programs correlate with higher performance
- Expected scores for new schools

---

## 💻 Ready-to-Run Scripts

### Quick Analysis Script

Save this as `analyze_education.py`:

```python
from scripts.utils import load_csv
import pandas as pd

# Load data
sat = load_csv("zt9s-n5aj_20251006_114228.csv")
demo = load_csv("s3k6-pzi2_20251006_114239.csv")

# Prepare SAT data
for col in ['mathematics_mean', 'critical_reading_mean', 'writing_mean', 'number_of_test_takers']:
    sat[col] = pd.to_numeric(sat[col], errors='coerce')

sat['total_score'] = sat[['mathematics_mean', 'critical_reading_mean', 'writing_mean']].sum(axis=1)

# Merge with demographics
analysis = sat.merge(demo[['dbn', 'boro']], on='dbn', how='left')

# Analysis
print("\n📊 NYC SAT Score Analysis\n")
print(f"Total Schools: {len(sat)}")
print(f"Average Total SAT: {sat['total_score'].mean():.0f}")

print("\n🗽 Scores by Borough:")
borough_avg = analysis.groupby('boro')['total_score'].mean().sort_values(ascending=False)
for boro, score in borough_avg.items():
    print(f"   {boro}: {score:.0f}")

print("\n🏆 Top 5 Schools:")
for idx, row in sat.nlargest(5, 'total_score').iterrows():
    print(f"   {row['school_name']}: {row['total_score']:.0f}")

print("\n📈 Performance Categories:")
high = len(sat[sat['total_score'] >= 1500])
med = len(sat[(sat['total_score'] >= 1200) & (sat['total_score'] < 1500)])
low = len(sat[sat['total_score'] < 1200])
print(f"   High (1500+): {high} schools ({high/len(sat)*100:.1f}%)")
print(f"   Medium (1200-1499): {med} schools ({med/len(sat)*100:.1f}%)")
print(f"   Below Average (<1200): {low} schools ({low/len(sat)*100:.1f}%)")
```

Then run: `python analyze_education.py`

---

## 📓 Interactive Notebook

Create a new notebook `nyc_education_analysis.ipynb` and start with:

```python
# Cell 1: Setup
from scripts.utils import load_csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set_style('whitegrid')

# Cell 2: Load Data
sat = load_csv("zt9s-n5aj_20251006_114228.csv")
demo = load_csv("s3k6-pzi2_20251006_114239.csv")

print(f"SAT Data: {len(sat)} schools")
print(f"Demographics: {len(demo)} schools")

# Cell 3: Explore
sat.head()

# Cell 4: Visualize
sat['total_score'] = pd.to_numeric(sat[['mathematics_mean', 'critical_reading_mean', 'writing_mean']].apply(pd.to_numeric, errors='coerce').sum(axis=1))
sat['total_score'].hist(bins=30, figsize=(10, 6))
plt.title('Distribution of Total SAT Scores')
plt.xlabel('Total Score')
plt.ylabel('Number of Schools')
plt.show()
```

---

## 🔍 Explore Demographics

The demographics file has **343 columns**! Here are some interesting ones:

- `school_name`, `dbn`, `boro` - Basic info
- `overview_paragraph` - School description
- `academicopportunities1`, `academicopportunities2` - Programs
- `ell_programs` - English language learner programs
- `neighborhood` - Location details
- Various demographic breakdowns

To explore:

```python
demo = load_csv("s3k6-pzi2_20251006_114239.csv")
print(demo.columns.tolist())  # See all columns
print(demo.dtypes)  # See data types
```

---

## 🎯 Next Steps

**Immediate (5 minutes):**

```powershell
# Run the analysis script we created
python scripts/analyze_nyc_education.py
```

**Quick Analysis (15 minutes):**

```powershell
# Create and run a custom analysis
python analyze_education.py
```

**Deep Dive (1+ hour):**

- Open a new Jupyter notebook
- Merge SAT scores with demographics
- Create visualizations
- Build correlations and insights

**Try More Data:**

```powershell
# Fetch math test results (might work now)
python scripts/fetch_data_gov.py 7yc5-fec2 --domain data.cityofnewyork.us --limit 500

# Or try recent math results
python scripts/fetch_data_gov.py ufu2-qea8 --domain data.cityofnewyork.us --limit 500
```

---

## 📚 Resources

- **Dataset Portal**: <https://opendata.cityofnewyork.us/>
- **Your Analysis Script**: `scripts/analyze_nyc_education.py`
- **List More Datasets**: `scripts/list_nyc_education.py`
- **Fetch More Data**: `scripts/fetch_data_gov.py`

---

## 🎊 Success

You now have rich NYC education data ready for analysis:

- ✅ 460 schools with SAT scores
- ✅ 440 schools with demographics (343 data points each!)
- ✅ Top school: Stuyvesant (2,087 total)
- ✅ Borough breakdown available
- ✅ Ready for visualization and modeling

**Start exploring your data! 🚀**
