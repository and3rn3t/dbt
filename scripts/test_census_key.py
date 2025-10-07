#!/usr/bin/env python3
"""Quick test of Census API key."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CENSUS_API_KEY")

print("\n" + "=" * 80)
print("CENSUS API KEY TEST")
print("=" * 80)

if not api_key:
    print("\n❌ No CENSUS_API_KEY found in .env file")
    print("\nAdd to .env:")
    print("   CENSUS_API_KEY=your_key_here")
else:
    print(f"\n✓ API Key found: {api_key[:10]}...")

    # Test with simple query
    print("\nTesting API key with Census Bureau...")
    url = "https://api.census.gov/data/2021/acs/acs5"
    params = {
        "get": "NAME,B01001_001E",
        "for": "county:163",
        "in": "state:19",
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✓ API key is working!")
            print(f"Response: {response.text[:200]}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print()
print()
print()
print()
print()
