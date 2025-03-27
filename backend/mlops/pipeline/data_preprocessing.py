from preprocessing.data_preprocessor_pipeline import DataPreprocessingPipeline
from preprocessing.data_cleaner import ColumnCleaner, DataFlattener
from preprocessing.data_normalizer import DataNormalizer
import pandas as pd

def filered_df():
    df = pd.read_csv("backend/mlops/data/raw/accInfo.csv")
    df = df[df.columns.difference(df.filter(like="id").columns[:3])]
    return df
def process(df):
    pipeline = DataPreprocessingPipeline([
        ("column_cleaner", ColumnCleaner(null_threshold=0.5)),
        ("flattener", DataFlattener()),
        ("column_cleaner", ColumnCleaner(null_threshold=0.99)),
    ])
    processed_df = pipeline.transform(df)
    print("\nProcessed Data:")
    print(processed_df.head())
    return processed_df
def main():
    df = filered_df()
    print(df.head())
    df = process(df)
    df.to_csv("backend/mlops/data/processed/test_3.csv", index=False)
    #df.to_csv("backend/mlops/data/processed/cleaned_accInfo.csv", index=False)
if __name__ == "__main__":
    main()