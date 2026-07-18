"""
Utility functions.

This module contains reusable helper functions for data inspection
and validation.
"""

import pandas as pd


def dataframe_summary(dataframe: pd.DataFrame, dataset_name: str) -> None:
    """
    Print a summary of a pandas DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataset to inspect.

    dataset_name : str
        Name of the dataset.
    """

    print("=" * 60)
    print(dataset_name.upper())
    print("=" * 60)

    print(f"Rows: {len(dataframe):,}")
    print(f"Columns: {len(dataframe.columns)}")
    print(f"Duplicates: {dataframe.duplicated().sum()}")

    print("\nMissing values:")

    print(dataframe.isna().sum())

    print("\n")
