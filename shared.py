"""
Shared data and utilities for Sidebot.
"""

import pandas as pd
import duckdb
import os

# Path to tips.csv (assume root of py-sidebot)
TIPS_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tips.csv')

def load_tips():
    """Load tips.csv, add percent column, and register with duckdb."""
    df = pd.read_csv(TIPS_CSV_PATH)
    df['percent'] = df['tip'] / df['total_bill']
    # Register DataFrame with duckdb as 'tips'
    con = duckdb.connect()
    con.register('tips', df)
    return df, con

tips, duckdb_con = load_tips()
__all__ = ["tips", "duckdb_con"]
