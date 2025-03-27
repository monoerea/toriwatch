from abc import ABC, abstractmethod
import pandas as pd
import json
import ast
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# --- Abstract Preprocessing Step ---
class PreprocessingStep(ABC):
    """Abstract class for a preprocessing step in the pipeline."""
    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

# --- Data Cleaner Parent Class ---import json
import ast
import pandas as pd
from tqdm import tqdm

class DataCleaner:
    """Base class for data cleaning operations."""
    
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement the process method")

# --- Data Flattening (Cleaning Step) ---
class DataFlattener(DataCleaner):
    """Processes JSON-like nested columns in a DataFrame."""

    def _safe_parse(self, value):
        """Safely parses JSON-like strings into Python objects."""
        if isinstance(value, str) and value[0] in "{[":
            try:
                return json.loads(value.replace("'", '"'))  # Convert single quotes to double for valid JSON
            except json.JSONDecodeError:
                try:
                    return json.loads(json.dumps(ast.literal_eval(value)))  # Fallback to ast.literal_eval
                except (ValueError, SyntaxError):
                    pass  
        return value  # Return unchanged if parsing fails

    def _process_item(self, key, value, parent_key, sep, items):
        """Processes and flattens a nested item into the result dictionary."""
        new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)
        if isinstance(value, (dict, list)):
            items.update(self._flatten(value, new_key, sep))
        else:
            items[new_key] = value

    def _flatten(self, data, parent_key='', sep='_'):
        """Flattens nested dictionaries and lists into a single-level dictionary."""
        items = {}

        if isinstance(data, (dict, list)):
            elements = data.items() if isinstance(data, dict) else enumerate(data)
            for key, value in elements:
                self._process_item(key, value, parent_key, sep, items)
        else:
            items[parent_key] = data

        return items

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parses and flattens all object columns that contain nested structures."""
        obj_cols = df.select_dtypes(include=['object']).columns
        new_columns = {}

        for col in tqdm(obj_cols, desc="Processing object columns"):
            df[col] = df[col].map(self._safe_parse)
            sample = next((x for x in df[col].dropna().values if isinstance(x, (dict, list))), None)

            if sample is not None:
                expanded_df = df[col].dropna().map(self._flatten).apply(pd.Series)
                new_columns[col] = expanded_df.add_prefix(f"{col}_")

        return pd.concat([df.drop(columns=new_columns.keys(), errors='ignore')] + list(new_columns.values()), axis=1) if new_columns else df



# --- General Column Cleanup (Duplicates, Nulls, Specified Columns) ---

class GenCleaner(DataCleaner):
    """Handles duplicate removal, null value handling, and dropping specified columns."""

    def __init__(self, columns_to_remove=None, null_threshold=0.5, column_for_deduplication=None):
        """
        :param columns_to_remove: List of columns to drop (default: None)
        :param null_threshold: Columns with more than this proportion of missing values will be dropped.
        """
        self.columns_to_remove = columns_to_remove or []
        self.null_threshold = null_threshold
        self.column_for_deduplication = column_for_deduplication

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # Remove duplicates
        if self.column_for_deduplication in df.columns:
            df = df.drop_duplicates(subset=self.column_for_deduplication, keep="first")
        df = df.loc[:, ~df.T.duplicated()]

        # Remove columns based on null threshold
        null_percent = df.isnull().mean()
        cols_to_drop = null_percent[null_percent > self.null_threshold].index.tolist()

        # Combine user-specified columns with high-null columns
        drop_list = list(set(self.columns_to_remove + cols_to_drop))

        # Ensure only valid columns are removed
        valid_drop_cols = [col for col in drop_list if col in df.columns]

        if valid_drop_cols:
            df = df.drop(columns=valid_drop_cols)
        else:
            print("⚠️ No valid columns to drop.")

        return df

# --- Data Normalization Factory ---
class NormalizerFactory:
    """Factory to create different types of normalizers."""

    NORMALIZERS = {
        "minmax": MinMaxScaler,
        "standard": StandardScaler,
        "robust": RobustScaler
    }

    @staticmethod
    def get_normalizer(normalizer_type="minmax"):
        if normalizer_type in NormalizerFactory.NORMALIZERS:
            return NormalizerFactory.NORMALIZERS[normalizer_type]()
        raise ValueError(f"Unsupported normalizer: {normalizer_type}")

# --- Data Normalization Step ---
class DataNormalizer(PreprocessingStep):
    """Applies user-selected normalization to specified numerical columns."""

    def __init__(self, columns=None, exclude_columns = None, normalizer_type="minmax"):
        self.columns = columns  # Columns to normalize (if None, normalize all numeric columns)
        self.exclude_columns = exclude_columns
        self.normalizer = NormalizerFactory.get_normalizer(normalizer_type)

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        numeric_cols = df.select_dtypes(include=['number']).columns
        if self.exclude_columns is not None:
            self.columns = numeric_cols.difference(self.exclude_columns)
        else:
            self.columns = numeric_cols

        if self.columns is not None and len(self.columns) > 0:
            df[self.columns] = self.normalizer.fit_transform(df[self.columns])

        return df
# --- Example Usage ---
def main():
    df = pd.read_csv("backend/mlops/data/raw/accInfo.csv")

    print("Original Data:")
    print(df.head())

    df = ColumnCleaner(null_threshold=0.5).process(df)
    df = DataFlattener().process(df)
    df = DataNormalizer(exclude_columns=["user_id"], normalizer_type="standard").process(df)

    print("\nProcessed Data:")
    print(df.to_csv("backend/mlops/data/processed/otherTest.csv", index=False))
    print(df.info())
if __name__ == "__main__":
    main()
