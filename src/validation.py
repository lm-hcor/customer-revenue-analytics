"""
Validation module.

This module contains data quality checks executed before loading
the datasets into PostgreSQL.
"""

from typing import Dict

import pandas as pd


def check_primary_key_duplicates(
    dataframe: pd.DataFrame,
    key_column: str,
    table_name: str,
) -> None:
    """
    Check whether a primary key contains duplicate values.
    """

    duplicates = dataframe[key_column].duplicated().sum()

    if duplicates == 0:
        print(f"✓ {table_name}: no duplicate values in '{key_column}'.")
    else:
        print(f"✗ {table_name}: {duplicates} duplicate values found in '{key_column}'.")


def check_foreign_key(
    child_dataframe: pd.DataFrame,
    child_column: str,
    parent_dataframe: pd.DataFrame,
    parent_column: str,
    relationship_name: str,
) -> None:
    """
    Check whether all foreign key values exist in the parent table.
    """

    missing = (
        ~child_dataframe[child_column].isin(parent_dataframe[parent_column])
    ).sum()

    if missing == 0:
        print(f"✓ {relationship_name}: referential integrity OK.")
    else:
        print(f"✗ {relationship_name}: {missing} orphan records detected.")


def validate_datasets(datasets: Dict[str, pd.DataFrame]) -> None:
    """
    Run all validation checks.
    """

    print("\nRunning data quality checks...\n")

    check_primary_key_duplicates(
        datasets["customers"],
        "customer_id",
        "customers",
    )

    check_primary_key_duplicates(
        datasets["orders"],
        "order_id",
        "orders",
    )

    check_primary_key_duplicates(
        datasets["products"],
        "product_id",
        "products",
    )

    check_foreign_key(
        datasets["orders"],
        "customer_id",
        datasets["customers"],
        "customer_id",
        "orders -> customers",
    )

    check_foreign_key(
        datasets["order_items"],
        "product_id",
        datasets["products"],
        "product_id",
        "order_items -> products",
    )

    check_foreign_key(
        datasets["payments"],
        "order_id",
        datasets["orders"],
        "order_id",
        "payments -> orders",
    )

    check_foreign_key(
        datasets["order_items"],
        "order_id",
        datasets["orders"],
        "order_id",
        "order_items -> orders",
    )
