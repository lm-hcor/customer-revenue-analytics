"""
Load module.

This module loads the transformed datasets into PostgreSQL.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

from database import get_engine
from extract import load_datasets
from transform import transform_datasets


# =============================================================================
# Functions
# =============================================================================

def load_table(engine, table_name, dataframe):
    """
    Load a pandas DataFrame into PostgreSQL.
    """

    print(f"\nLoading {table_name}...")

    dataframe.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"✓ {table_name} loaded ({len(dataframe):,} rows)")


# =============================================================================
# Main
# =============================================================================

def main():

    engine = get_engine()

    datasets = load_datasets()

    transformed = transform_datasets(datasets)

    load_order = [
        "categories",
        "products",
        "customers",
        "orders",
        "payments",
        "order_items",
    ]

    for table in load_order:

        load_table(
            engine,
            table,
            transformed[table],
        )

    print("\n" + "=" * 60)
    print("ETL completed successfully.")
    print("=" * 60)


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    main()