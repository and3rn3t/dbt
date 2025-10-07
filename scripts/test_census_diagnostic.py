#!/usr/bin/env python3
"""Test Census API with different endpoints."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CENSUS_API_KEY")

print("\n" + "=" * 80)
print("CENSUS API DIAGNOSTIC TEST")
print("=" * 80)
print(f"API Key: {api_key[:15]}...\n")

# Test 1: Simple state query
print("Test 1: Simple state population query...")
url = "https://api.census.gov/data/2021/acs/acs5"
params = {"get": "NAME,B01001_001E", "for": "state:19", "key": api_key}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        if response.text.startswith("<"):
            print(f"  ❌ Got HTML response (Invalid Key)")
            print(f"  Response: {response.text[:300]}")
        else:
            print(f"  ✓ Got JSON response")
            print(f"  Data: {response.text[:200]}")
    else:
        print(f"  ❌ Error: {response.text[:200]}")
except Exception as e:
    print(f"  ❌ Exception: {str(e)}")

# Test 2: Without API key (to see if it's a key issue)
print("\nTest 2: Same query WITHOUT API key...")
params_no_key = {"get": "NAME,B01001_001E", "for": "state:19"}

try:
    response = requests.get(url, params=params_no_key, timeout=10)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ Works without key!")
        print(f"  Data: {response.text[:200]}")
    else:
        print(f"  ❌ Error: {response.text[:200]}")
except Exception as e:
    print(f"  ❌ Exception: {str(e)}")

# Test 3: Different year
print("\nTest 3: Try 2020 ACS...")
url_2020 = "https://api.census.gov/data/2020/acs/acs5"
params_2020 = {"get": "NAME,B01001_001E", "for": "state:19"}

try:
    response = requests.get(url_2020, params=params_2020, timeout=10)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ 2020 works!")
        print(f"  Data: {response.text[:200]}")
except Exception as e:
    print(f"  ❌ Exception: {str(e)}")

print("\n" + "=" * 80)
print("RECOMMENDATION:")
print("=" * 80)
print("\nThe Census API key might:")
print("  1. Need time to activate (wait 5-10 minutes after signup)")
print("  2. Have been copied incorrectly (check for extra spaces)")
print("  3. Be from the wrong site (should be api.census.gov)")
print("\nTry fetching without the key for now (slower but works):")
print("  Edit fetch_scott_county_census.py to make key optional")
print()
print()
print()
print()
print()
