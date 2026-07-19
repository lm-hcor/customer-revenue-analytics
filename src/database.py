"""
Database configuration.

This module creates the connection to PostgreSQL.

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

load_dotenv(dotenv_path=ENV_PATH, override=True)


# =============================================================================
# Database connection
# =============================================================================

def get_engine() -> Engine:
    """
    Create and return a SQLAlchemy engine.
    """

    connection_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    return create_engine(connection_string)