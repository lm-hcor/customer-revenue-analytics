"""
Load module.

This module loads the transformed datasets into PostgreSQL.

Author: Luis Miguel Herrera
Project: Customer Revenue Analytics
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


# =============================================================================
# Load environment variables
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

if not ENV_PATH.exists():
    raise FileNotFoundError(f".env file not found: {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH, override=True)


# =============================================================================
# Database connection
# =============================================================================

def create_database_engine() -> Engine:
    """
    Create a SQLAlchemy engine for PostgreSQL.
    """

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, port, database, user, password]):
        raise ValueError(
            "One or more environment variables are missing. "
            "Check your .env file."
        )

    connection_string = (
        f"postgresql+psycopg2://"
        f"{user}:{password}@{host}:{port}/{database}"
    )

    return create_engine(connection_string)


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """
    Test the connection to PostgreSQL.
    """

    engine = create_database_engine()

    with engine.connect():
        print("Successfully connected to PostgreSQL.")


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    main()