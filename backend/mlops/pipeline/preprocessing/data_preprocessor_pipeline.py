from typing import List, Tuple
import pandas as pd

class PreprocessingStep:
    """Base class for preprocessing steps."""
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Each step must implement this method."""
        raise NotImplementedError

class DataPreprocessingPipeline:
    """Pipeline that applies multiple preprocessing steps in sequence."""

    def __init__(self, steps: List[Tuple[str, PreprocessingStep]]):
        """
        :param steps: List of tuples (name, transformer), where transformer is an instance of a processing class.
        """
        self.steps = steps

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies each step sequentially on the DataFrame."""
        df = df.copy()  # Ensure the original df isn't modified
        for name, step in self.steps:
            print(f"Applying step: {name} | DataFrame shape before: {df.shape}")  # Debugging log
            df = step.process(df.copy())  # Pass a copy to avoid in-place modification issues
            if df is None or not isinstance(df, pd.DataFrame):
                raise ValueError(f"Step '{name}' returned None or an invalid object. Ensure all process methods return a DataFrame.")

            print(f"Completed step: {name} | DataFrame shape after: {df.shape}")  # Debugging log
            print(df.head())  # Debugging output after each step

        return df
