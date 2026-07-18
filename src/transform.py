"""
Transform module.

This module is responsible for cleaning and preparing all datasets
before loading them into PostgreSQL.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

from typing import Dict

import pandas as pd

from extract import load_datasets
from utils import dataframe_summary
from validation import validate_datasets


# =============================================================================
# Cleaning functions
# =============================================================================


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the customers dataset.
    """

    customers = customers.drop_duplicates().reset_index(drop=True)

    dataframe_summary(customers, "Customers")

    return customers


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the orders dataset.
    """

    orders = orders.drop_duplicates().reset_index(drop=True)

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(orders[column])

    dataframe_summary(orders, "Orders")

    return orders


def clean_order_items(order_items: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the order items dataset.
    """

    order_items = order_items.drop_duplicates().reset_index(drop=True)

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"]
    )

    dataframe_summary(order_items, "Order Items")

    return order_items


def clean_payments(payments: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the payments dataset.
    """

    payments = payments.drop_duplicates().reset_index(drop=True)

    dataframe_summary(payments, "Payments")

    return payments


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the products dataset.
    """

    products = products.drop_duplicates().reset_index(drop=True)

    dataframe_summary(products, "Products")

    return products


def clean_categories(categories: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the category translation dataset.
    """

    categories = categories.drop_duplicates().reset_index(drop=True)

    dataframe_summary(categories, "Categories")

    return categories


# =============================================================================
# Transformation pipeline
# =============================================================================


def transform_datasets(
    datasets: Dict[str, pd.DataFrame],
) -> Dict[str, pd.DataFrame]:
    """
    Apply all cleaning functions.
    """

    transformed = {}

    transformed["customers"] = clean_customers(datasets["customers"])
    transformed["orders"] = clean_orders(datasets["orders"])
    transformed["order_items"] = clean_order_items(datasets["order_items"])
    transformed["payments"] = clean_payments(datasets["payments"])
    transformed["products"] = clean_products(datasets["products"])
    transformed["categories"] = clean_categories(datasets["categories"])

    return transformed


def main() -> None:
    """
    Execute the transformation pipeline.
    """

    datasets = load_datasets()

    transformed = transform_datasets(datasets)
    validate_datasets(transformed)

    print("=" * 60)
    print(f"Successfully transformed {len(transformed)} datasets.")
    print("=" * 60)


if __name__ == "__main__":
    main()
