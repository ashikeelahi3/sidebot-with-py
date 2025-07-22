"""
Query logic and LLM prompt engineering for Sidebot.
"""
import pandas as pd

def df_to_schema(df: pd.DataFrame) -> str:
    """Generate a schema description from a DataFrame."""
    lines = [f"- {col}: {dtype}" for col, dtype in zip(df.columns, df.dtypes)]
    return '\n'.join(lines)

def system_prompt(df: pd.DataFrame, prompt_path: str = "prompt.md") -> str:
    """Read prompt.md and inject the generated schema."""
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    schema = df_to_schema(df)
    return prompt.replace("${SCHEMA}", schema)
