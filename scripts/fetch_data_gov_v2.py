#!/usr/bin/env python3
"""
Fetch data from data.gov using the Socrata API.
Now with automatic API token support for higher rate limits!

Usage:
    python fetch_data_gov.py <dataset_id> [--limit N] [--domain DOMAIN]

Examples:
    python fetch_data_gov.py kzjm-xkqj --limit 10000
    python fetch_data_gov.py vbim-akqf --domain chronicdata.cdc.gov --limit 5000
"""

import sys
import os
import argparse
from sodapy import Socrata
import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (including API token)
load_dotenv()


def setup_directories():
    """Ensure data directories exist."""
    directories = ["data/raw", "data/staging", "data/processed", "data/external"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✓ Data directories ready")


def fetch_dataset(dataset_id, limit=10000, domain="data.seattle.gov", app_token=None):
    """
    Fetch a dataset from data.gov using Socrata API.

    Args:
        dataset_id: The Socrata dataset identifier
        limit: Maximum number of records to fetch
        domain: The Socrata domain (default: Seattle)
        app_token: Optional API token (automatically loaded from .env)

    Returns:
        pandas DataFrame with fetched data
    """
    print(f"\n{'='*60}")
    print(f"Fetching dataset: {dataset_id}")
    print(f"Domain: {domain}")
    print(f"Limit: {limit:,} records")
    if app_token:
        print(f"✓ Using API token (higher rate limits - 1,000 req/hour)")
    else:
        print(f"⚠️  No API token (rate limited - ~100 req/hour)")
        print(f"   Get a free token at: https://{domain}/profile/app_tokens")
    print(f"{'='*60}\n")

    try:
        # Create client with optional token
        client = Socrata(domain, app_token)

        # Fetch the data
        print("Downloading data...")
        results = client.get(dataset_id, limit=limit)

        if not results:
            print("⚠ No data returned. Check dataset ID.")
            return None

        # Convert to pandas DataFrame
        df = pd.DataFrame.from_records(results)

        print(f"✓ Downloaded {len(df):,} records")
        print(f"✓ Columns ({len(df.columns)}): {', '.join(df.columns.tolist()[:10])}")
        if len(df.columns) > 10:
            print(f"  ... and {len(df.columns) - 10} more columns")

        return df

    except Exception as e:
        print(f"❌ Error fetching data: {str(e)}")
        return None


def save_data(df, dataset_id, output_dir="data/raw"):
    """
    Save data to the data lake.

    Args:
        df: DataFrame to save
        dataset_id: Identifier for naming the file
        output_dir: Directory to save to

    Returns:
        Path to saved file
    """
    if df is None or df.empty:
        print("⚠ No data to save")
        return None

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/{dataset_id}_{timestamp}.csv"

    print(f"\nSaving data...")
    df.to_csv(output_file, index=False)

    file_size_kb = os.path.getsize(output_file) / 1024
    file_size_mb = file_size_kb / 1024

    print(f"✓ Saved to: {output_file}")
    print(f"✓ Records: {len(df):,}")
    print(f"✓ Size: {file_size_mb:.2f} MB ({file_size_kb:.2f} KB)")

    return output_file


def show_preview(df):
    """Show a preview of the data."""
    if df is None or df.empty:
        return

    print(f"\n{'='*60}")
    print("Data Preview (first 5 rows):")
    print(f"{'='*60}\n")
    print(df.head().to_string())

    print(f"\n{'='*60}")
    print("Data Types:")
    print(f"{'='*60}\n")
    print(df.dtypes)

    print(f"\n{'='*60}")
    print("Basic Statistics:")
    print(f"{'='*60}\n")
    print(df.describe())


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Fetch data from data.gov and save to data lake",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (TESTED & WORKING):
  python fetch_data_gov.py kzjm-xkqj --domain data.seattle.gov              # Seattle Police
  python fetch_data_gov.py kzjm-xkqj --domain data.seattle.gov --limit 100  # Limit records
  python fetch_data_gov.py vbim-akqf --domain chronicdata.cdc.gov           # CDC COVID Data
  
Popular Dataset IDs (TESTED & WORKING):
  kzjm-xkqj  Seattle Police Reports (data.seattle.gov)
  vbim-akqf  CDC COVID-19 Data (chronicdata.cdc.gov)
  
Note: NYC Open Data may require API token or have connection issues

API Token:
  Add to .env file: DATA_GOV_APP_TOKEN=your_token_here
  Get free token at: https://data.seattle.gov/profile/app_tokens
        """,
    )

    parser.add_argument(
        "dataset_id", help="Socrata dataset identifier (e.g., kzjm-xkqj)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10000,
        help="Maximum number of records to fetch (default: 10000)",
    )
    parser.add_argument(
        "--domain",
        default="data.seattle.gov",
        help="Socrata domain (default: data.seattle.gov - TESTED & WORKING)",
    )
    parser.add_argument(
        "--preview", action="store_true", help="Show data preview after fetching"
    )
    parser.add_argument(
        "--output-dir", default="data/raw", help="Output directory (default: data/raw)"
    )
    parser.add_argument("--token", help="API token (optional, can also use .env file)")

    args = parser.parse_args()

    try:
        # Setup
        setup_directories()

        # Get token from args or environment
        token = args.token or os.getenv("DATA_GOV_APP_TOKEN")

        # Fetch data
        df = fetch_dataset(args.dataset_id, args.limit, args.domain, token)

        if df is None:
            sys.exit(1)

        # Show preview if requested
        if args.preview:
            show_preview(df)

        # Save data
        output_file = save_data(df, args.dataset_id, args.output_dir)

        if output_file:
            print(f"\n{'='*60}")
            print("✓ Success! Next Steps:")
            print(f"{'='*60}\n")
            print(f"1. Review the data:")
            print(f"   pandas: pd.read_csv('{output_file}')")
            print(f"   duckdb: SELECT * FROM read_csv_auto('{output_file}') LIMIT 10;")
            print(f"\n2. Create a staging model:")
            print(f"   cp templates/staging_model_template.sql \\")
            print(f"      dbt_project/models/staging/stg_{args.dataset_id}.sql")
            print(f"\n3. Run dbt pipeline:")
            print(f"   cd dbt_project && dbt run --select stg_{args.dataset_id}")

            if not token:
                print(f"\n💡 Tip: Get a free API token for 10x higher rate limits!")
                print(f"   Visit: https://{args.domain}/profile/app_tokens")

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
