# How to Get and Use data.gov API Tokens

## Why You Need an API Token

### Without Token (Current State)

- ⚠️ **Rate Limited**: Strict throttling on requests
- ⚠️ **Slower**: Limited to fewer requests per hour
- ⚠️ **Warning Messages**: `Requests made without an app_token will be subject to strict throttling limits`
- ✅ **Works**: But with limitations

### With Token (Recommended)

- ✅ **Higher Limits**: 1,000 requests per rolling hour (vs ~100 without)
- ✅ **Faster**: No throttling warnings
- ✅ **Better Performance**: Priority queue
- ✅ **Free**: No cost for reasonable use

---

## Step-by-Step: Getting Your API Token

### Method 1: Socrata Open Data Portal (Recommended)

#### Step 1: Visit the Registration Page

Go to: **<https://data.seattle.gov/profile/app_tokens>**

Or for NYC: **<https://data.cityofnewyork.us/profile/app_tokens>**

(Most Socrata portals use the same login system)

#### Step 2: Create an Account

1. Click **"Sign Up"** (top right)
2. Choose one of these options:
   - Sign up with email
   - Sign in with Google
   - Sign in with GitHub
3. Verify your email address

#### Step 3: Generate App Token

1. Once logged in, go to **"Developer Settings"** or **"App Tokens"**
2. Click **"Create New App Token"**
3. Fill in the form:
   - **Application Name**: "Personal Data Hub" (or your project name)
   - **Description**: "Data analysis and exploration"
   - **Application Website**: (optional - can be your GitHub)
4. Click **"Create Token"**

#### Step 4: Save Your Token

You'll receive:

- **App Token**: A string like `aBc123XyZ789...`
- **Key ID**: A unique identifier
- **Secret**: Keep this private!

**⚠️ IMPORTANT**: Copy and save these immediately! You may not be able to see them again.

---

## Using Your API Token

### Method 1: In Python Code

```python
from sodapy import Socrata

# With authentication
client = Socrata(
    "data.seattle.gov",
    app_token="YOUR_TOKEN_HERE",  # Your app token
    username="your.email@example.com",  # Optional
    password="your_password"  # Optional
)

# Fetch data (with higher rate limits!)
results = client.get("kzjm-xkqj", limit=10000)
```

### Method 2: Environment Variables (Recommended)

#### Create `.env` file

```bash
# In your workspace root
cd C:\Users\and3r\Documents\data-science-workspace

# Create .env file
echo "DATA_GOV_APP_TOKEN=your_actual_token_here" > .env
```

#### Use in Python

```python
import os
from dotenv import load_dotenv
from sodapy import Socrata

# Load environment variables
load_dotenv()

# Use token from environment
client = Socrata(
    "data.seattle.gov",
    app_token=os.getenv("DATA_GOV_APP_TOKEN")
)

results = client.get("kzjm-xkqj", limit=10000)
```

#### Use in fetch_data_gov.py

```python
# Already set up! Just add to .env:
# DATA_GOV_APP_TOKEN=your_token_here

# The script will automatically use it
python fetch_data_gov.py kzjm-xkqj --limit 10000
```

### Method 3: Command Line Argument

Update `fetch_data_gov.py` to accept token as argument:

```python
parser.add_argument(
    '--token',
    help='Socrata API app token (optional, for higher rate limits)'
)

# Then use it:
client = Socrata(domain, args.token)
```

Usage:

```bash
python fetch_data_gov.py kzjm-xkqj --token YOUR_TOKEN_HERE
```

---

## Quick Setup Guide

### 1. Install python-dotenv

```bash
pip install python-dotenv
```

### 2. Create .env file

```bash
# In your workspace directory
cd C:\Users\and3r\Documents\data-science-workspace
```

Create a file named `.env` with:

```
DATA_GOV_APP_TOKEN=your_actual_token_here
```

### 3. Update your code

Add to the top of your Python scripts:

```python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DATA_GOV_APP_TOKEN")
```

### 4. Use the token

```python
from sodapy import Socrata

client = Socrata("data.seattle.gov", token)
# Now you have higher rate limits!
```

---

## Updating fetch_data_gov.py to Use Token

Here's the updated function:

```python
def fetch_dataset(dataset_id, limit=10000, domain="data.seattle.gov", app_token=None):
    """
    Fetch a dataset from data.gov using Socrata API.
    
    Args:
        dataset_id: The Socrata dataset identifier
        limit: Maximum number of records to fetch
        domain: The Socrata domain
        app_token: Optional API token for higher rate limits
    """
    print(f"\n{'='*60}")
    print(f"Fetching dataset: {dataset_id}")
    print(f"Domain: {domain}")
    print(f"Limit: {limit:,} records")
    if app_token:
        print(f"✓ Using API token (higher rate limits)")
    else:
        print(f"⚠️ No token (rate limited)")
    print(f"{'='*60}\n")
    
    try:
        # Create client with optional token
        client = Socrata(domain, app_token)
        
        # Rest of the code...
```

---

## Token Security Best Practices

### ✅ DO

- Store tokens in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables
- Keep tokens private
- Rotate tokens periodically

### ❌ DON'T

- Commit tokens to Git
- Share tokens publicly
- Hard-code tokens in scripts
- Share screenshots with tokens visible

---

## Testing Your Token

### Simple Test Script

```python
from sodapy import Socrata
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DATA_GOV_APP_TOKEN")

print(f"Token loaded: {'✓ Yes' if token else '✗ No'}")

if token:
    try:
        client = Socrata("data.seattle.gov", token)
        results = client.get("kzjm-xkqj", limit=10)
        print(f"✓ Token works! Fetched {len(results)} records")
    except Exception as e:
        print(f"✗ Token error: {e}")
else:
    print("⚠️ No token found in .env file")
```

Save as `test_token.py` and run:

```bash
python test_token.py
```

---

## Rate Limits Reference

| Limit Type | Without Token | With Token |
|------------|--------------|------------|
| Requests/hour | ~100 | 1,000 |
| Requests/day | ~1,000 | 10,000+ |
| Concurrent requests | 1 | 4 |
| Priority | Low | Normal |

---

## Troubleshooting

### Problem: "Invalid app token"

**Solution**:

- Check token is copied correctly (no extra spaces)
- Verify token is active in your Socrata account
- Try regenerating the token

### Problem: Token not loading from .env

**Solution**:

```python
# Debug script
import os
from dotenv import load_dotenv

load_dotenv()
print(f"Current directory: {os.getcwd()}")
print(f"Token: {os.getenv('DATA_GOV_APP_TOKEN')}")

# Check if .env file exists
print(f".env exists: {os.path.exists('.env')}")
```

### Problem: Still getting rate limited

**Solution**:

- Verify token is being passed to Socrata client
- Check token hasn't expired
- Add delays between requests: `time.sleep(1)`

---

## Different Portals = Different Tokens?

### Single Sign-On

Most Socrata portals (data.gov ecosystem) use the **same account system**:

- One account works across most portals
- One token works across most portals
- Register once, use everywhere

### Supported Portals (Same Token)

- data.seattle.gov ✓
- data.cityofnewyork.us ✓
- data.cityofchicago.org ✓
- data.wa.gov ✓
- data.ct.gov ✓
- Many more...

### Separate Systems

- chronicdata.cdc.gov (different system)
- Some specialized portals may have their own auth

---

## Example .env File

```bash
# data.gov API Configuration
DATA_GOV_APP_TOKEN=aBc123XyZ789ExampleToken456

# Optional: For authenticated requests
# DATA_GOV_USERNAME=your.email@example.com
# DATA_GOV_PASSWORD=your_password

# Database configuration
DATABASE_PATH=data/personal_data_hub.duckdb

# Environment
ENVIRONMENT=development
```

---

## Quick Commands

```bash
# Create .env file
echo "DATA_GOV_APP_TOKEN=your_token_here" > .env

# Test token
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DATA_GOV_APP_TOKEN'))"

# Fetch data with token (if implemented)
python fetch_data_gov.py kzjm-xkqj --limit 10000

# Install dotenv
pip install python-dotenv
```

---

## Resources

- **Socrata API Docs**: <https://dev.socrata.com/docs/app-tokens.html>
- **Register for Token**: <https://data.seattle.gov/profile/app_tokens>
- **Rate Limits**: <https://dev.socrata.com/docs/app-tokens.html#rate-limits>
- **sodapy Documentation**: <https://github.com/xmunoz/sodapy>

---

## Summary

1. **Register**: Create account at any Socrata portal (e.g., data.seattle.gov)
2. **Generate**: Create app token in Developer Settings
3. **Store**: Save token in `.env` file
4. **Use**: Load with `python-dotenv` and pass to Socrata client
5. **Enjoy**: 10x higher rate limits! 🚀

**Total setup time**: ~5 minutes  
**Cost**: Free  
**Benefit**: Much faster and more reliable data fetching!

---

## Need Help?

- Check token status: Login to portal → Developer Settings
- Test token: Run `test_token.py` (see above)
- Questions: Socrata developer forum or documentation

**You don't need a token to get started**, but it's highly recommended for production use!
