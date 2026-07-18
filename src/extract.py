"""
Extract module.

This module is responsible for loading all raw datasets used in the
Customer Revenue Analytics project.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

from pathlib import Path
from typing import Dict

import pandas as pd


# =============================================================================
# Configuration
# =============================================================================

# Directory containing all raw CSV files
RAW_DATA_PATH = Path("data/raw")

# Mapping between logical dataset names and CSV filenames
DATASETS = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "categories": "product_category_name_translation.csv",
}


# =============================================================================
# Functions
# =============================================================================


def load_datasets() -> Dict[str, pd.DataFrame]:
    """
    Load all raw CSV files into a dictionary of pandas DataFrames.

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary where:
            - key: dataset name
            - value: pandas DataFrame
    """

    loaded_datasets = {}

    for dataset_name, filename in DATASETS.items():
        file_path = RAW_DATA_PATH / filename

        print(f"Loading {filename}...")

        dataframe = pd.read_csv(file_path)

        loaded_datasets[dataset_name] = dataframe

        rows, columns = dataframe.shape

        print(f"Loaded {rows:,} rows and {columns} columns.\n")

    return loaded_datasets


def main() -> None:
    """
    Execute the extraction process.
    """

    loaded_datasets = load_datasets()

    print("=" * 60)
    print(f"Successfully loaded {len(loaded_datasets)} datasets.")
    print("=" * 60)


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    main()
