"""
Quick test to verify your data.gov API token is working
"""
import os
from dotenv import load_dotenv
from sodapy import Socrata

print("="*60)
print("Data.gov API Token Test")
print("="*60)

# Load environment variables
load_dotenv()
token = os.getenv("DATA_GOV_APP_TOKEN")

# Check if token exists
print(f"\n1. Token Status:")
if token:
    print(f"   ✓ Token found: {token[:10]}...{token[-4:]}")
else:
    print(f"   ✗ No token found")
    print(f"   → Create a .env file with: DATA_GOV_APP_TOKEN=your_token_here")

# Test without token
print(f"\n2. Testing WITHOUT token (rate limited):")
try:
    client = Socrata("data.seattle.gov", None)
    results = client.get("kzjm-xkqj", limit=5)
    print(f"   ✓ Fetched {len(results)} records (but with rate limits)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test with token (if available)
if token:
    print(f"\n3. Testing WITH token (higher limits):")
    try:
        client = Socrata("data.seattle.gov", token)
        results = client.get("kzjm-xkqj", limit=5)
        print(f"   ✓ Token works! Fetched {len(results)} records")
        print(f"   ✓ You now have 10x higher rate limits!")
    except Exception as e:
        print(f"   ✗ Token error: {e}")
        print(f"   → Check your token is valid and active")

print(f"\n" + "="*60)
print("Summary:")
print("="*60)
if token:
    print("✓ You're all set! Use your token for faster data fetching.")
else:
    print("ℹ️  You can still fetch data without a token (just slower).")
    print("   Get a free token at: https://data.seattle.gov/profile/app_tokens")
print("="*60)
