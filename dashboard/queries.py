"""
Database queries for the dashboard.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# =============================================================================
# Database connection
# =============================================================================

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


# =============================================================================
# Load analytical views
# =============================================================================

def load_sales_summary() -> pd.DataFrame:
    """Load sales summary."""
    return pd.read_sql(
        "SELECT * FROM vw_sales_summary;",
        engine
    )


def load_customer_metrics() -> pd.DataFrame:
    """Load customer metrics."""
    return pd.read_sql(
        "SELECT * FROM vw_customer_metrics;",
        engine
    )


def load_category_metrics() -> pd.DataFrame:
    """Load category metrics."""
    return pd.read_sql(
        """
        SELECT *
        FROM vw_category_metrics
        ORDER BY revenue DESC;
        """,
        engine
    )

def load_monthly_revenue() -> pd.DataFrame:
    """Load monthly revenue."""
    return pd.read_sql(
        """
        SELECT *
        FROM vw_monthly_revenue
        ORDER BY month;
        """,
        engine
    )


def load_payment_metrics() -> pd.DataFrame:
    """Load payment metrics."""
    return pd.read_sql(
        """
        SELECT *
        FROM vw_payment_metrics
        ORDER BY total_payments DESC;
        """,
        engine
    )


def load_delivery_performance() -> pd.DataFrame:
    """Load delivery performance."""
    return pd.read_sql(
        "SELECT * FROM vw_delivery_performance;",
        engine
    )


# =============================================================================
# Dashboard KPIs
# =============================================================================

def load_kpis() -> dict:
    """
    Compute dashboard KPIs.
    """

    sales = load_sales_summary()
    customers = load_customer_metrics()

    return {

        "total_revenue": sales["total_revenue"].sum(),

        "total_orders": sales["order_id"].nunique(),

        "total_customers": customers["customer_unique_id"].nunique(),

        "average_order_value": sales["total_revenue"].mean()

    }


# =============================================================================
# Test
# =============================================================================

def main():

    print("Dashboard queries started\n")

    print(load_monthly_revenue().head())

    print("\nKPIs\n")

    print(load_kpis())

    print("\nFinished")


if __name__ == "__main__":
    main()
