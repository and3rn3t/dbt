# Getting API Tokens for data.gov - Quick Guide

## 🎯 Quick Answer

**5-Minute Setup:**

1. **Visit**: <https://data.seattle.gov/profile/app_tokens>
2. **Sign Up**: Create a free account (or sign in with Google/GitHub)
3. **Generate Token**: Click "Create New App Token"
4. **Save Token**: Copy it to a `.env` file

---

## Why Get a Token?

| Feature | Without Token | With Token |
|---------|--------------|------------|
| Requests/hour | ~100 | 1,000 |
| Speed | Slower | Faster |
| Warnings | Yes | No |
| Cost | Free | Free |

**Bottom line**: 10x more requests, no throttling warnings, still free!

---

## Step-by-Step Instructions

### 1. Create Account (2 minutes)

Go to any Socrata portal and sign up:

- **Seattle**: <https://data.seattle.gov>
- **NYC**: <https://data.cityofnewyork.us>
- **Chicago**: <https://data.cityofchicago.org>

Click **"Sign Up"** → Use email or Google/GitHub login

### 2. Generate Token (1 minute)

1. After logging in, click your profile → **"Developer Settings"**
2. Or go directly to: <https://data.seattle.gov/profile/app_tokens>
3. Click **"Create New App Token"**
4. Fill in:
   - **Name**: "Personal Data Hub"
   - **Description**: "Data analysis project"
5. Click **"Save"**

### 3. Copy Your Token

You'll see something like:

```
App Token: aBc123XyZ789ExampleToken456
```

**⚠️ Save this immediately!**

### 4. Add to .env File (1 minute)

Create a file named `.env` in your workspace:

```bash
DATA_GOV_APP_TOKEN=aBc123XyZ789ExampleToken456
```

**That's it!** Your scripts will now use the token automatically.

---

## Using Your Token

### In Python

```python
import os
from dotenv import load_dotenv
from sodapy import Socrata

# Load token from .env
load_dotenv()
token = os.getenv("DATA_GOV_APP_TOKEN")

# Use it
client = Socrata("data.seattle.gov", token)
results = client.get("kzjm-xkqj", limit=10000)  # Much higher limits!
```

### Test It

```bash
# Install python-dotenv first
pip install python-dotenv

# Test your token
python test_token.py
```

---

## Important Notes

### ✅ DO

- Store token in `.env` file
- Add `.env` to `.gitignore`
- Keep token private

### ❌ DON'T

- Commit token to Git
- Share token publicly
- Hard-code in scripts

---

## One Token, Multiple Portals

Good news! **One token works across most Socrata portals**:

- ✅ data.seattle.gov
- ✅ data.cityofnewyork.us
- ✅ data.cityofchicago.org
- ✅ Most data.gov ecosystem sites

Register once, use everywhere!

---

## Troubleshooting

### "Where do I create the .env file?"

In your workspace directory:

```bash
cd C:\Users\and3r\Documents\data-science-workspace
notepad .env
```

Then add:

```
DATA_GOV_APP_TOKEN=your_actual_token_here
```

### "How do I know it's working?"

Run the test script:

```bash
python test_token.py
```

You should see:

```
✓ Token found: aBc123XyZ7...
✓ Token works! Fetched 5 records
✓ You now have 10x higher rate limits!
```

---

## Resources

- **Get Token**: <https://data.seattle.gov/profile/app_tokens>
- **API Docs**: <https://dev.socrata.com/docs/app-tokens.html>
- **Full Guide**: See `API_TOKEN_GUIDE.md`

---

## Summary

**Time**: 5 minutes  
**Cost**: Free  
**Benefit**: 10x faster data fetching

**You don't need a token to start**, but it's highly recommended for regular use!

---

## Quick Start

```bash
# 1. Create .env file
echo "DATA_GOV_APP_TOKEN=your_token_here" > .env

# 2. Install dotenv
pip install python-dotenv

# 3. Test it
python test_token.py

# 4. Use it
python fetch_data_gov.py kzjm-xkqj --limit 10000
```

**Done!** 🎉
