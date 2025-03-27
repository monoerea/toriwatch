import pandas as pd
import json
import ast
from tqdm import tqdm
class DataNormalizer:
    def __init__(self, df):
        self.df = df.copy()

    def normalize(self):
        """Placeholder for generic normalization tasks."""
        return self.df

class NestedDataFlattener(DataNormalizer):
    def __init__(self, df):
        self.df = df.copy()

    def _safe_parse(self, value):
        """Safely parses JSON-like strings into Python objects."""
        if isinstance(value, str) and (value.startswith("{") or value.startswith("[")):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(value)  # Handle Python-style dicts
                except (ValueError, SyntaxError):
                    return value  # Return as is if parsing fails
        return value

    def _flatten(self, data, parent_key='', sep='_'):
        """Recursively flattens dictionaries and lists into a single-level dictionary."""
        items = {}
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, (dict, list)):
                    items.update(self._flatten(v, new_key, sep))
                else:
                    items[new_key] = v
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                if isinstance(item, (dict, list)):
                    items.update(self._flatten(item, new_key, sep))
                else:
                    items[new_key] = item
        else:
            items[parent_key] = data
        return items

    def flatten_columns(self):
        """Flattens all object columns that contain nested structures efficiently."""
        obj_cols = self.df.select_dtypes(include=['object']).columns
        new_columns = {}

        for col in tqdm(obj_cols, desc="Flattening object columns"):
            # Step 1: Parse potential JSON strings
            self.df[col] = self.df[col].map(self._safe_parse)

            # Step 2: Identify nested structures
            sample = self.df[col].dropna().iloc[0] if not self.df[col].dropna().empty else None
            if isinstance(sample, (dict, list)):
                expanded_df = self.df[col].dropna().map(self._flatten).apply(pd.Series)
                expanded_df = expanded_df.add_prefix(f"{col}_")
                new_columns[col] = expanded_df

        # Efficiently merge new columns without fragmentation
        if new_columns:
            self.df = pd.concat([self.df] + list(new_columns.values()), axis=1)

        return self.df

    def remove_nested_columns(self):
        """Drops original nested columns after flattening."""
        obj_cols = self.df.select_dtypes(include=['object']).columns
        drop_cols = [col for col in obj_cols if self.df[col].apply(lambda x: isinstance(x, (dict, list))).any()]
        self.df.drop(columns=drop_cols, inplace=True)
        return self.df

    def preprocess(self):
        """Runs the full preprocessing pipeline."""
        self.flatten_columns()
        self.remove_nested_columns()
        self.df = self.df.loc[:, ~self.df.T.duplicated()]
        return self.df
class DataCleaner:
    """Base class for data cleaning operations."""
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement the process method")
class DataFlattener(DataCleaner):
    """Flattens JSON-like nested columns in a DataFrame."""

    def _safe_parse(self, value):
        """Safely parses JSON-like strings into Python objects."""
        if isinstance(value, str) and (value.startswith("{") or value.startswith("[")):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(value)  # Handle Python-style dicts
                except (ValueError, SyntaxError):
                    return value  # Return as is if parsing fails
        return value

    def _flatten(self, data, parent_key='', sep='_'):
        """Recursively flattens dictionaries and lists into a single-level dictionary."""
        items = {}
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, (dict, list)):
                    items.update(self._flatten(v, new_key, sep))
                else:
                    items[new_key] = v
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                if isinstance(item, (dict, list)):
                    items.update(self._flatten(item, new_key, sep))
                else:
                    items[new_key] = item
        else:
            items[parent_key] = data
        return items

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flattens all object columns that contain nested structures."""
        obj_cols = df.select_dtypes(include=['object']).columns
        new_columns = {}

        for col in tqdm(obj_cols, desc="Flattening object columns"):
            # Step 1: Parse potential JSON strings
            df[col] = df[col].map(self._safe_parse)

            # Step 2: Identify nested structures
            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
            if isinstance(sample, (dict, list)):
                expanded_df = df[col].dropna().map(self._flatten).apply(pd.Series)
                expanded_df = expanded_df.add_prefix(f"{col}_")
                new_columns[col] = expanded_df

        # Efficiently merge new columns without fragmentation
        if new_columns:
            df = pd.concat([df] + list(new_columns.values()), axis=1)

        return df
# Example usage:
df_cleaned = pd.read_csv("backend/mlops/data/raw/accInfo.csv")
pipeline = [
    DataFlattener(),
]

for step in pipeline:
    df = step.process(df_cleaned)

# Save processed DataFrame
    df.to_csv("backend/mlops/data/processed/test2.csv", index=False)
    print("Preprocessing complete. Final dataframe shape:", df.shape)
    print("Sample data:")
    print(df.head())