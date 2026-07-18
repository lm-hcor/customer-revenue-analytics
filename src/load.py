"""
Load module.

This module loads the transformed datasets into PostgreSQL.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")


def create_database_engine() -> Engine:
    """
    Create a SQLAlchemy engine.
    """

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    connection_string = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    engine = create_engine(connection_string)

    return engine


def main() -> None:
    """
    Execute the loading process.
    """

    engine = create_database_engine()

    with engine.connect():
        print("Successfully connected to PostgreSQL.")


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    main()
