"""
Check if city-level Census data is available within Scott County, Iowa.

The Census Bureau has data at different geographic levels:
- State
- County
- Place (cities/towns)
- Tract
- Block Group

This script checks what's available for Scott County.
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

STATE_FIPS = "19"  # Iowa
COUNTY_FIPS = "163"  # Scott County


def check_places_in_county():
    """
    Check available places (cities) in Scott County.

    Note: Places may cross county boundaries, so we'll check all Iowa places
    and filter those that overlap with Scott County.
    """
    print("\n" + "=" * 80)
    print("CHECKING PLACES (CITIES/TOWNS) IN SCOTT COUNTY, IOWA")
    print("=" * 80)

    # Get all places in Iowa
    url = (
        f"https://api.census.gov/data/2021/acs/acs5"
        f"?get=NAME"
        f"&for=place:*"
        f"&in=state:{STATE_FIPS}"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        places = [row[0] for row in data[1:]]

        print(f"\nFound {len(places)} places in Iowa")
        print("\nMajor cities in Scott County area:")

        # Scott County includes these major cities
        scott_county_cities = [
            "Bettendorf",
            "Davenport",
            "Eldridge",
            "Blue Grass",
            "Buffalo",
            "Dixon",
            "Durant",
            "Le Claire",
            "Long Grove",
            "McCausland",
            "Panorama Park",
            "Princeton",
            "Riverdale",
            "Walcott",
        ]

        found_cities = []
        for city_name in scott_county_cities:
            matches = [p for p in places if city_name.lower() in p.lower()]
            if matches:
                for match in matches:
                    print(f"  - {match}")
                    found_cities.append(match)

        if found_cities:
            print(f"\n✓ Found {len(found_cities)} cities in Scott County")
            print(
                "\nYou can fetch data for these cities using the 'place' geography level."
            )
        else:
            print("\n✗ No cities found (this might be an API limitation)")

        return found_cities

    except Exception as e:
        print(f"Error: {e}")
        return []


def check_tracts_in_county():
    """Check census tracts in Scott County."""
    print("\n" + "=" * 80)
    print("CHECKING CENSUS TRACTS IN SCOTT COUNTY")
    print("=" * 80)

    # Get tracts in Scott County
    url = (
        f"https://api.census.gov/data/2021/acs/acs5"
        f"?get=NAME,B01003_001E"  # Include population
        f"&for=tract:*"
        f"&in=state:{STATE_FIPS}%20county:{COUNTY_FIPS}"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        tracts = data[1:]

        print(f"\n✓ Found {len(tracts)} census tracts in Scott County")
        print("\nSample tracts:")
        for tract in tracts[:5]:
            name = tract[0]
            pop = int(tract[1]) if tract[1] else 0
            tract_id = tract[4]
            print(f"  Tract {tract_id}: {name} (Pop: {pop:,})")

        if len(tracts) > 5:
            print(f"  ... and {len(tracts) - 5} more tracts")

        print("\nCensus tracts are smaller geographic areas within the county.")
        print("Each tract typically contains 1,200-8,000 people.")

        return tracts

    except Exception as e:
        print(f"Error: {e}")
        return []


def explain_geographies():
    """Explain different geographic levels available."""
    print("\n" + "=" * 80)
    print("CENSUS GEOGRAPHY LEVELS")
    print("=" * 80)

    print(
        """
Available geography levels for Scott County analysis:

1. COUNTY LEVEL (what we have now)
   - Scott County as a whole
   - Best for county-wide trends
   - Easiest to compare with state

2. PLACE LEVEL (cities/towns)
   - Individual cities like Davenport, Bettendorf, etc.
   - Good for comparing cities within the county
   - May include areas outside the county boundary

3. TRACT LEVEL (census tracts)
   - Smaller neighborhoods within the county
   - ~30-40 tracts in Scott County
   - Best for identifying within-county variation
   - More granular than cities

4. BLOCK GROUP LEVEL (very detailed)
   - Smallest geographic unit with detailed stats
   - 600-3,000 people per block group
   - Most granular analysis possible

RECOMMENDATION:
- For city comparison: Use PLACE level for major cities
- For neighborhood analysis: Use TRACT level
- For very detailed mapping: Use BLOCK GROUP level
    """
    )


def show_next_steps():
    """Show next steps for city-level analysis."""
    print("\n" + "=" * 80)
    print("NEXT STEPS FOR CITY-LEVEL ANALYSIS")
    print("=" * 80)

    print(
        """
To fetch data for cities in Scott County:

1. Fetch data for major cities:
   python scripts/fetch_scott_county_cities.py

2. Compare cities within the county:
   python scripts/compare_cities.py

3. Map tract-level data:
   python scripts/analyze_tracts.py

Would you like me to create these scripts?
    """
    )


def main():
    """Main execution function."""
    explain_geographies()

    cities = check_places_in_county()
    tracts = check_tracts_in_county()

    show_next_steps()

    if cities:
        print(f"\n✓ City-level data IS available for Scott County")
    if tracts:
        print(f"✓ Tract-level data IS available ({len(tracts)} tracts)")


if __name__ == "__main__":
    main()
    main()
    main()
    main()
    main()
