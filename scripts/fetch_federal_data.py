#!/usr/bin/env python3
"""
Fetch popular federal datasets from Data.gov

Quick access to CDC, EPA, BLS, and other federal data sources.

Usage:
    python scripts/fetch_federal_data.py --list              # Show all available datasets
    python scripts/fetch_federal_data.py --dataset cdc-covid # Fetch specific dataset
    python scripts/fetch_federal_data.py --category health   # Fetch all health datasets
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sodapy import Socrata

# Load environment variables
load_dotenv()


# Federal Dataset Catalog
FEDERAL_DATASETS = {
    "health": {
        "cdc-covid": {
            "id": "vbim-akqf",
            "domain": "chronicdata.cdc.gov",
            "name": "CDC COVID-19 Case Surveillance",
            "description": "COVID-19 case data from CDC surveillance",
            "size": "Millions",
        },
        "chronic-disease": {
            "id": "9mfq-cb36",
            "domain": "chronicdata.cdc.gov",
            "name": "Chronic Disease Indicators",
            "description": "Health outcomes and risk factors by state",
            "size": "100K+",
        },
        "obesity": {
            "id": "cjae-szjv",
            "domain": "chronicdata.cdc.gov",
            "name": "Nutrition, Physical Activity, and Obesity",
            "description": "Obesity and health behavior data",
            "size": "50K+",
        },
        "brfss": {
            "id": "735e-byxc",
            "domain": "chronicdata.cdc.gov",
            "name": "Behavioral Risk Factor Surveillance System",
            "description": "Annual health survey data",
            "size": "400K+",
        },
    },
    "crime": {
        "seattle-police": {
            "id": "kzjm-xkqj",
            "domain": "data.seattle.gov",
            "name": "Seattle Police Reports",
            "description": "Police incident reports with location data",
            "size": "100K+",
        },
    },
}


def list_datasets():
    """Display all available datasets organized by category."""
    print("\n" + "=" * 80)
    print("FEDERAL DATASETS - Quick Access Catalog")
    print("=" * 80 + "\n")

    for category, datasets in FEDERAL_DATASETS.items():
        print(f"📁 {category.upper()}")
        print("-" * 80)

        for key, info in datasets.items():
            print(f"\n  🔹 {key}")
            print(f"     Name: {info['name']}")
            print(f"     Description: {info['description']}")
            print(f"     Dataset ID: {info['id']}")
            print(f"     Domain: {info['domain']}")
            print(f"     Size: {info['size']}")
            print(f"\n     Fetch: python scripts/fetch_federal_data.py --dataset {key}")

        print()

    print("=" * 80)
    print("\n💡 TIP: Get API token from https://api.data.gov/signup/ for faster access")
    print("   Add to .env file: DATA_GOV_APP_TOKEN=your_token_here\n")


def fetch_dataset(dataset_key, limit=10000, preview=False):
    """
    Fetch a federal dataset by key.

    Args:
        dataset_key: Short key from FEDERAL_DATASETS catalog
        limit: Maximum records to fetch
        preview: Show data preview after fetching
    """
    # Find dataset in catalog
    dataset_info = None
    for category, datasets in FEDERAL_DATASETS.items():
        if dataset_key in datasets:
            dataset_info = datasets[dataset_key]
            break

    if not dataset_info:
        print(f"❌ Dataset '{dataset_key}' not found in catalog")
        print(f"   Run with --list to see available datasets")
        return None

    print("\n" + "=" * 80)
    print(f"FETCHING: {dataset_info['name']}")
    print("=" * 80)
    print(f"Dataset ID: {dataset_info['id']}")
    print(f"Domain: {dataset_info['domain']}")
    print(f"Description: {dataset_info['description']}")
    print(f"Limit: {limit:,} records")
    print("=" * 80 + "\n")

    try:
        # Get API token
        app_token = os.getenv("DATA_GOV_APP_TOKEN")
        if app_token:
            print("✓ Using API token for higher rate limits")
        else:
            print("⚠ No API token - using public access (slower)")
            print("  Get token: https://api.data.gov/signup/")

        # Create Socrata client
        client = Socrata(dataset_info["domain"], app_token)

        # Fetch data
        print("\nDownloading data...")
        results = client.get(dataset_info["id"], limit=limit)

        if not results:
            print("⚠ No data returned")
            return None

        # Convert to DataFrame
        df = pd.DataFrame.from_records(results)

        print(f"\n✓ Downloaded {len(df):,} records")
        print(f"✓ Columns ({len(df.columns)}): {', '.join(df.columns.tolist()[:8])}")
        if len(df.columns) > 8:
            print(f"  ... and {len(df.columns) - 8} more columns")

        # Show preview if requested
        if preview:
            print("\n" + "=" * 80)
            print("DATA PREVIEW (first 5 rows)")
            print("=" * 80 + "\n")
            print(df.head())

            print("\n" + "=" * 80)
            print("DATA TYPES")
            print("=" * 80 + "\n")
            print(df.dtypes)

        # Save data
        output_dir = Path("data/raw")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"{dataset_key}_{timestamp}.csv"

        print(f"\nSaving data...")
        df.to_csv(output_file, index=False)

        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"✓ Saved to: {output_file}")
        print(f"✓ Size: {file_size_mb:.2f} MB")

        # Show next steps
        print("\n" + "=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print(f"\n1. Load in Python:")
        print(f"   import pandas as pd")
        print(f"   df = pd.read_csv('{output_file}')")
        print(f"\n2. Explore in Jupyter:")
        print(f"   jupyter lab")
        print(f"\n3. Create dbt staging model:")
        print(f"   See templates/ directory for examples")
        print()

        return df

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def fetch_category(category, limit=5000):
    """Fetch all datasets in a category."""
    if category not in FEDERAL_DATASETS:
        print(f"❌ Category '{category}' not found")
        print(f"   Available: {', '.join(FEDERAL_DATASETS.keys())}")
        return

    datasets = FEDERAL_DATASETS[category]
    print(f"\n📦 Fetching all datasets in category: {category.upper()}")
    print(f"   Total datasets: {len(datasets)}")
    print(f"   Limit per dataset: {limit:,} records\n")

    results = {}
    for key in datasets.keys():
        print(f"\n{'='*80}")
        print(f"Dataset {list(datasets.keys()).index(key) + 1}/{len(datasets)}")
        print(f"{'='*80}")
        df = fetch_dataset(key, limit=limit, preview=False)
        if df is not None:
            results[key] = len(df)

    print("\n" + "=" * 80)
    print("CATEGORY FETCH COMPLETE")
    print("=" * 80)
    for key, rows in results.items():
        print(f"  ✓ {key}: {rows:,} records")
    print()


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Fetch federal datasets from Data.gov",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available datasets
  python scripts/fetch_federal_data.py --list

  # Fetch specific dataset
  python scripts/fetch_federal_data.py --dataset cdc-covid --limit 10000

  # Fetch with preview
  python scripts/fetch_federal_data.py --dataset chronic-disease --preview

  # Fetch entire category
  python scripts/fetch_federal_data.py --category health --limit 5000

Popular Datasets:
  cdc-covid          CDC COVID-19 case surveillance data
  chronic-disease    Chronic disease indicators by state
  obesity            Nutrition and obesity data
  seattle-police     Seattle police incident reports

Categories:
  health             Public health datasets (CDC)
  crime              Law enforcement data
        """,
    )

    parser.add_argument(
        "--list", action="store_true", help="List all available datasets"
    )
    parser.add_argument("--dataset", help="Dataset key to fetch (e.g., cdc-covid)")
    parser.add_argument(
        "--category", help="Fetch all datasets in a category (e.g., health)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10000,
        help="Maximum records to fetch (default: 10000)",
    )
    parser.add_argument(
        "--preview", action="store_true", help="Show data preview after fetching"
    )

    args = parser.parse_args()

    # Show usage if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n💡 TIP: Start with --list to see available datasets\n")
        sys.exit(0)

    try:
        if args.list:
            list_datasets()
        elif args.dataset:
            fetch_dataset(args.dataset, args.limit, args.preview)
        elif args.category:
            fetch_category(args.category, args.limit)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
