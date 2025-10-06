# Data.gov Quick Start - Resume Your Work 🚀

## ✅ What's Already Set Up

Your Data.gov integration is **fully functional**:

- ✅ **API Token**: Configured in `.env` (10x faster requests!)
- ✅ **sodapy**: Installed and working
- ✅ **Token Tested**: Successfully fetched 500 records
- ✅ **Scripts Ready**: `fetch_data_gov.py` and `fetch_data_gov_v2.py`

## 🎯 Quick Examples

### 1. Fetch Seattle Police Reports

```powershell
python scripts/fetch_data_gov.py kzjm-xkqj --domain data.seattle.gov --limit 1000
```

### 2. Fetch NYC 311 Service Requests

```powershell
python scripts/fetch_data_gov.py erm2-nwe9 --domain data.cityofnewyork.us --limit 1000
```

### 3. Fetch CDC COVID Data

```powershell
python scripts/fetch_data_gov.py vbim-akqf --domain chronicdata.cdc.gov --limit 500
```

## 📊 Popular Datasets

### Seattle Open Data (data.seattle.gov)

- **kzjm-xkqj** - Police Report Incidents
- **33kz-ixgy** - Building Permits
- **65db-xm6k** - Real Time Fire 911 Calls

### NYC Open Data (data.cityofnewyork.us)

- **erm2-nwe9** - 311 Service Requests
- **25th-nujf** - Motor Vehicle Collisions
- **h9gi-nx95** - NYPD Complaint Data

### CDC Data (chronicdata.cdc.gov)

- **vbim-akqf** - COVID-19 Case Surveillance
- **csmm-fdhi** - PLACES Health Data
- **mr8w-325u** - Life Expectancy at Birth

## 🔍 Explore Datasets

Visit these portals to find more:

- **Seattle**: <https://data.seattle.gov/browse>
- **NYC**: <https://opendata.cityofnewyork.us/>
- **Chicago**: <https://data.cityofchicago.org/>
- **National**: <https://catalog.data.gov/dataset>

Look for the **dataset ID** in the URL or "API" section.

## 💻 Use in Python

### Quick Analysis Script

```python
from sodapy import Socrata
import pandas as pd
import os
from dotenv import load_dotenv

# Load API token
load_dotenv()
token = os.getenv("DATA_GOV_APP_TOKEN")

# Connect with your token
client = Socrata("data.seattle.gov", token)

# Fetch data
results = client.get("kzjm-xkqj", limit=1000)
df = pd.DataFrame.from_records(results)

# Analyze
print(f"Total incidents: {len(df)}")
print(f"\nTop 5 incident types:")
print(df['type'].value_counts().head())

# Save
df.to_csv("data/raw/seattle_police.csv", index=False)
```

### With Utility Functions

```python
from scripts.utils import load_csv, save_csv
import pandas as pd

# Load freshly fetched data
df = load_csv("kzjm-xkqj_20251006_113843.csv")

# Analyze
incident_counts = df.groupby('type').size().sort_values(ascending=False)

# Save analysis
save_csv(
    incident_counts.to_frame('count'),
    "incident_analysis.csv",
    subfolder="processed"
)
```

## 📓 Interactive Notebook

Open your existing notebook:

```powershell
# In VS Code, click:
test_datagov_notebook.ipynb
```

This notebook has:

- ✅ Examples of fetching different datasets
- ✅ Data cleaning workflows
- ✅ Visualization examples
- ✅ Error handling patterns

## 🔧 Advanced Usage

### Fetch with Filters

```python
from sodapy import Socrata
from dotenv import load_dotenv
import os

load_dotenv()
client = Socrata("data.seattle.gov", os.getenv("DATA_GOV_APP_TOKEN"))

# Filter by date and type
results = client.get(
    "kzjm-xkqj",
    where="datetime > '2024-01-01' AND type='BURGLARY'",
    limit=5000
)
```

### Pagination for Large Datasets

```python
from sodapy import Socrata
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
client = Socrata("data.seattle.gov", os.getenv("DATA_GOV_APP_TOKEN"))

# Fetch in chunks
all_data = []
offset = 0
limit = 1000

while True:
    results = client.get("kzjm-xkqj", limit=limit, offset=offset)
    if not results:
        break
    all_data.extend(results)
    offset += limit
    print(f"Fetched {len(all_data)} records...")

    if len(all_data) >= 10000:  # Stop at 10k
        break

df = pd.DataFrame.from_records(all_data)
```

## 🚨 Troubleshooting

### "ModuleNotFoundError: No module named 'sodapy'"

```powershell
pip install sodapy
```

### Token Not Working

1. Check `.env` file has: `DATA_GOV_APP_TOKEN=your_token_here`
2. No quotes around the token
3. No spaces before/after the `=`
4. Run: `python test_token.py` to verify

### Rate Limiting Errors

- Your token gives you **1,000 requests/hour**
- Without token: only ~100 requests/hour
- Solution: Make sure `.env` is loaded (`load_dotenv()`)

### Dataset Not Found

- Verify the dataset ID from the data portal URL
- Check you're using the correct domain
- Some datasets require special permissions

## 📚 Documentation

Check your `docs/` folder:

- **DATA_GOV_GUIDE.md** - Complete guide with tested examples
- **QUICK_TOKEN_GUIDE.md** - How to get and use tokens
- **API_TOKEN_GUIDE.md** - Detailed token documentation
- **DATAGOV_IMPLEMENTATION.md** - Technical details

## 🎯 What to Do Next

**Option 1: Fetch Fresh Data**

```powershell
python scripts/fetch_data_gov.py kzjm-xkqj --domain data.seattle.gov --limit 2000
```

**Option 2: Analyze Existing Data**

```powershell
python scripts/example_analysis.py
```

**Option 3: Open Interactive Notebook**
Click: `test_datagov_notebook.ipynb` in VS Code

**Option 4: Explore New Datasets**
Visit: <https://data.seattle.gov/browse>
Find a dataset ID and fetch it!

---

## 🔥 Quick Test

Run this to verify everything works:

```powershell
# Test your token
python test_token.py

# Fetch some data
python scripts/fetch_data_gov.py kzjm-xkqj --domain data.seattle.gov --limit 100

# Analyze it
python scripts/example_analysis.py
```

**You're all set to work with Data.gov!** 🎉
