# --- Data Normalization Factory ---
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

from .data_preprocessor_pipeline import PreprocessingStep


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