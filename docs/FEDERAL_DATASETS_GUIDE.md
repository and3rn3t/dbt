# Federal Open Data Guide 🇺🇸

Complete guide to accessing federal government datasets through Data.gov and Socrata Open Data API.

## 🎯 Quick Start

```powershell
# Fetch federal data
python scripts/fetch_data_gov.py <dataset_id> --domain <domain> --limit 1000
```

---

## 📊 Major Federal Data Sources

### 1. **Centers for Disease Control (CDC)**

**Domain:** `chronicdata.cdc.gov` | `data.cdc.gov`

#### Available Datasets

| Dataset ID  | Name                                       | Records  | Topics                      |
| ----------- | ------------------------------------------ | -------- | --------------------------- |
| `vbim-akqf` | COVID-19 Case Surveillance                 | Millions | Epidemiology, public health |
| `9mfq-cb36` | Chronic Disease Indicators                 | 100K+    | Health outcomes, prevention |
| `cjae-szjv` | Nutrition, Physical Activity, and Obesity  | 50K+     | Health behaviors            |
| `735e-byxc` | Behavioral Risk Factor Surveillance System | 400K+    | Health surveys              |

**Example:**

```python
python scripts/fetch_data_gov.py vbim-akqf --domain chronicdata.cdc.gov --limit 5000
```

**Use Cases:**

- Public health analysis
- Disease pattern tracking
- Geographic health disparities
- Time series epidemiology
- Risk factor analysis

---

### 2. **Bureau of Labor Statistics (BLS)**

**Domain:** `data.bls.gov`

#### Key Datasets

- **Unemployment rates by state/county**
- **Consumer Price Index (CPI)**
- **Employment statistics**
- **Wage data by occupation**
- **Industry employment trends**

**Note:** BLS primarily uses their own API. Use:

```python
# Install BLS API client
pip install bls-api-client

from bls import BLS
bls = BLS(api_key='YOUR_KEY')
data = bls.get_series('LAUCN040010000000005')  # Unemployment rate
```

---

### 3. **Census Bureau**

**Domain:** `api.census.gov`

#### Popular Datasets

| Dataset       | Name                      | Description                      |
| ------------- | ------------------------- | -------------------------------- |
| ACS           | American Community Survey | Demographics, income, housing    |
| Decennial     | Decennial Census          | Population counts every 10 years |
| Economic      | Economic Census           | Business statistics              |
| International | International Trade Data  | Import/export data               |

**Example:**

```python
# Census API (requires API key from census.gov/developers)
import requests

# Get population by state
url = "https://api.census.gov/data/2020/dec/pl"
params = {
    'get': 'NAME,P1_001N',  # State name and population
    'for': 'state:*',
    'key': 'YOUR_API_KEY'
}
response = requests.get(url, params=params)
data = response.json()
```

**Use Cases:**

- Demographic analysis
- Income inequality studies
- Housing market analysis
- Population forecasting
- Economic development

---

### 4. **Environmental Protection Agency (EPA)**

**Domain:** `edg.epa.gov` | Various EPA databases

#### Key Data

- **Air Quality System (AQS):** Air pollution measurements
- **Toxic Release Inventory (TRI):** Industrial chemical releases
- **Enforcement and Compliance:** Violations and penalties
- **Water Quality:** Drinking water safety data

**Example:**

```python
# EPA AQS API
import requests

url = "https://aqs.epa.gov/data/api/dailyData/bySite"
params = {
    'email': 'your@email.com',
    'key': 'YOUR_KEY',
    'param': '88101',  # PM2.5
    'bdate': '20240101',
    'edate': '20241231',
    'state': '06',  # California
    'county': '037'  # Los Angeles
}
```

**Use Cases:**

- Air quality analysis
- Environmental health studies
- Climate change impact
- Industrial pollution tracking

---

### 5. **Department of Transportation (DOT)**

**Domain:** `data.transportation.gov`

#### Datasets

- **National Highway Traffic Safety:** Crash data
- **Aviation Safety:** Flight delays, incidents
- **Maritime Administration:** Shipping data
- **Federal Railroad Administration:** Rail safety

**Example Transportation Datasets:**

| Dataset                     | Description                 | Records  |
| --------------------------- | --------------------------- | -------- |
| Airline On-Time Performance | Flight delays/cancellations | Millions |
| Vehicle Crash Data          | Traffic accidents           | Millions |
| Bridge Inventory            | National bridge conditions  | 600K+    |

---

### 6. **Federal Emergency Management Agency (FEMA)**

**Domain:** `www.fema.gov/api` (REST API)

#### Key Data

- **Disaster Declarations:** Major disasters by state
- **NFIP Claims:** Flood insurance claims
- **Hazard Mitigation:** Grant programs
- **Individual Assistance:** Disaster aid applications

**Example:**

```python
import requests

url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
params = {'$filter': "state eq 'TX'"}
response = requests.get(url, params=params)
disasters = response.json()
```

**Use Cases:**

- Disaster impact analysis
- Climate risk assessment
- Emergency preparedness planning
- Economic disaster impact

---

### 7. **Department of Education**

**Domain:** `data.ed.gov`

#### Major Datasets

- **College Scorecard:** University data, costs, outcomes
- **IPEDS:** Higher education statistics
- **Civil Rights Data Collection:** K-12 equity data
- **National Assessment of Educational Progress (NAEP):** Student achievement

**Example - College Scorecard API:**

```python
import requests

url = "https://api.data.gov/ed/collegescorecard/v1/schools"
params = {
    'api_key': 'YOUR_KEY',
    'school.state': 'CA',
    'fields': 'school.name,2021.student.size,2021.admissions.admission_rate.overall'
}
response = requests.get(url, params=params)
colleges = response.json()
```

---

### 8. **Department of Energy (DOE)**

**Domain:** `www.eia.gov/opendata/` (Energy Information Administration)

#### Key Data

- **Electricity generation by source**
- **Natural gas prices and production**
- **Crude oil imports/exports**
- **Renewable energy statistics**
- **Carbon emissions**

**Example:**

```python
import requests

url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
headers = {'X-Params': '{"frequency":"daily","data":["value"],"facets":{},"start":"2024-01-01","end":"2024-12-31","sort":[{"column":"period","direction":"desc"}]}'}
headers['X-API-KEY'] = 'YOUR_KEY'
response = requests.get(url, headers=headers)
```

---

### 9. **National Oceanic and Atmospheric Administration (NOAA)**

**Domain:** `www.ncdc.noaa.gov/cdo-web/` | `api.weather.gov`

#### Datasets

- **Climate Data Online (CDO):** Historical weather
- **Global Historical Climatology Network:** Temperature records
- **National Water Model:** Streamflow, flooding
- **Sea Level Rise:** Coastal impact data

**Example - Weather Data:**

```python
import requests

# Get weather stations
url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
headers = {'token': 'YOUR_NOAA_TOKEN'}
params = {'locationid': 'FIPS:06', 'limit': 1000}
response = requests.get(url, headers=headers, params=params)
```

---

### 10. **Securities and Exchange Commission (SEC)**

**Domain:** `www.sec.gov/edgar`

#### Financial Data

- **EDGAR Database:** Public company filings (10-K, 10-Q, 8-K)
- **Mutual Fund Holdings**
- **Insider Trading Reports**
- **Corporate Actions**

**Example:**

```python
import requests
from sec_edgar_downloader import Downloader

# Download filings
dl = Downloader("MyCompanyName", "my.email@example.com")
dl.get("10-K", "AAPL", limit=5)
```

---

### 11. **National Institutes of Health (NIH)**

**Domain:** `clinicaltrials.gov/api/` | `pubmed.ncbi.nlm.nih.gov/`

#### Datasets

- **ClinicalTrials.gov:** Clinical trial data
- **PubMed:** Biomedical literature
- **GenBank:** Genetic sequences
- **dbGaP:** Genotype-phenotype associations

---

### 12. **Department of Agriculture (USDA)**

**Domain:** `quickstats.nass.usda.gov/api` (NASS QuickStats)

#### Key Data

- **Crop production and yields**
- **Livestock inventory**
- **Agricultural prices**
- **Farm economics**
- **Food security indicators**

---

## 🚀 Quick Fetch Examples

### Fetch CDC COVID Data

```powershell
python scripts/fetch_data_gov.py vbim-akqf --domain chronicdata.cdc.gov --limit 10000
```

### Fetch Multiple Datasets (Script)

```python
# scripts/fetch_federal_data.py
from sodapy import Socrata
import pandas as pd

datasets = [
    ("vbim-akqf", "chronicdata.cdc.gov", "cdc_covid"),
    ("9mfq-cb36", "chronicdata.cdc.gov", "chronic_disease"),
]

for dataset_id, domain, name in datasets:
    client = Socrata(domain, None)
    results = client.get(dataset_id, limit=5000)
    df = pd.DataFrame.from_records(results)
    df.to_csv(f"data/raw/{name}.csv", index=False)
    print(f"✓ Saved {name}: {len(df)} records")
```

---

## 🔑 Getting API Keys

Most federal APIs require free registration:

### 1. **Data.gov API Key** (Universal)

- Visit: <https://api.data.gov/signup/>
- Use across: CDC, EPA, DOE, Education
- Free, instant approval

### 2. **Census API Key**

- Visit: <https://api.census.gov/data/key_signup.html>
- Required for Census Bureau data
- Free, instant

### 3. **NOAA Token**

- Visit: <https://www.ncdc.noaa.gov/cdo-web/token>
- For Climate Data Online
- Free, email delivery

### 4. **BLS API Key**

- Visit: <https://data.bls.gov/registrationEngine/>
- Higher rate limits with key
- Free registration

---

## 💾 Store API Keys in .env

```bash
# .env file (NEVER commit this!)
DATA_GOV_APP_TOKEN=your_data_gov_key
CENSUS_API_KEY=your_census_key
NOAA_TOKEN=your_noaa_token
BLS_API_KEY=your_bls_key
```

**Load in Python:**

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('DATA_GOV_APP_TOKEN')
```

---

## 📋 Popular Federal Dataset Categories

### Economics & Labor

- ✅ Unemployment rates (BLS)
- ✅ GDP by state (Bureau of Economic Analysis)
- ✅ Inflation/CPI (BLS)
- ✅ International trade (Census)

### Health & Safety

- ✅ Disease surveillance (CDC)
- ✅ Drug safety (FDA)
- ✅ Hospital quality (CMS)
- ✅ Occupational safety (OSHA)

### Environment & Climate

- ✅ Air quality (EPA)
- ✅ Weather patterns (NOAA)
- ✅ Climate change (NOAA, NASA)
- ✅ Water quality (EPA, USGS)

### Demographics & Society

- ✅ Population statistics (Census)
- ✅ Crime data (FBI UCR)
- ✅ Education outcomes (Dept. of Education)
- ✅ Housing data (HUD)

### Energy & Transportation

- ✅ Electricity generation (EIA)
- ✅ Vehicle safety (NHTSA)
- ✅ Flight data (FAA)
- ✅ Fuel prices (EIA)

---

## 🛠️ Analysis Pipeline Template

```python
# 1. Fetch data
from sodapy import Socrata
import pandas as pd

client = Socrata("chronicdata.cdc.gov", os.getenv('DATA_GOV_APP_TOKEN'))
results = client.get("vbim-akqf", limit=10000)
df = pd.DataFrame.from_records(results)

# 2. Save raw data
df.to_csv("data/raw/cdc_covid.csv", index=False)

# 3. Basic cleaning
df_clean = df.dropna(subset=['critical_column'])
df_clean['date'] = pd.to_datetime(df_clean['date'])

# 4. Save processed data
df_clean.to_csv("data/processed/cdc_covid_clean.csv", index=False)

# 5. Analyze
summary = df_clean.groupby('state').agg({
    'cases': 'sum',
    'deaths': 'sum'
})

# 6. Visualize
import matplotlib.pyplot as plt
summary['cases'].plot(kind='bar', figsize=(12, 6))
plt.title('COVID Cases by State')
plt.savefig('docs/visualizations/covid_by_state.png')
```

---

## 📊 Sample Use Cases

### 1. Economic Dashboard

- BLS unemployment + Census demographics
- Track employment trends by region
- Correlate with education levels

### 2. Public Health Analysis

- CDC disease data + EPA air quality
- Find environmental health correlations
- Time series disease forecasting

### 3. Climate Impact Study

- NOAA weather + FEMA disasters
- Agricultural yields (USDA)
- Infrastructure damage patterns

### 4. Education Equity

- Dept of Education data + Census demographics
- Achievement gaps analysis
- Resource allocation patterns

---

## 🎯 Next Steps

1. **Choose Your Domain:**

   - Health? → Start with CDC
   - Economics? → Start with BLS/Census
   - Environment? → Start with EPA/NOAA

2. **Get API Keys:**

   - Visit api.data.gov for universal key
   - Register for specific agency keys

3. **Fetch Sample Data:**

   ```powershell
   python scripts/fetch_data_gov.py vbim-akqf --domain chronicdata.cdc.gov --limit 1000 --preview
   ```

4. **Explore in Notebook:**

   ```powershell
   jupyter lab notebooks/federal_data_exploration.ipynb
   ```

---

## 📚 Resources

- **Data.gov Catalog:** <https://catalog.data.gov/>
- **API Documentation:** <https://api.data.gov/docs/>
- **Socrata API Docs:** <https://dev.socrata.com/>
- **Federal Agency APIs:** <https://api.data.gov/docs/>

---

## ✅ What You Can Build

With federal data, you can create:

- 📊 **Economic dashboards** (unemployment, inflation, trade)
- 🏥 **Health surveillance systems** (disease tracking, outcomes)
- 🌍 **Climate analysis tools** (weather patterns, disasters)
- 🎓 **Education analytics** (achievement gaps, funding)
- 🚗 **Transportation insights** (safety, traffic, aviation)
- 🏭 **Environmental monitoring** (air/water quality, emissions)

**Start exploring federal data today!** 🚀
