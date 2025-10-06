# Scripts Directory

This directory contains reusable Python scripts for data automation and utilities.

## Structure

- **Data fetching scripts**: Scripts to retrieve data from APIs and external sources
- **Data processing utilities**: Common data transformation functions
- **Automation scripts**: Scheduled tasks and batch processing

## Usage

Move `fetch_data_gov.py` and `fetch_data_gov_v2.py` from the root directory to this folder for better organization.

## Example

```python
from scripts.fetch_data_gov import fetch_dataset

data = fetch_dataset('dataset-id')
```
