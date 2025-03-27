from preprocessing.data_preprocessor_pipeline import DataPreprocessingPipeline
from preprocessing.data_cleaner import GenCleaner, DataFlattener
from preprocessing.data_normalizer import DataNormalizer
import pandas as pd

def filered_df():
    df = pd.read_csv("backend/mlops/data/raw/accInfo.csv")
    df = df[["id"] + df.columns.difference(df.filter(like="id").columns[:3]).tolist()]
    return df
def tweet_process(df):
    pipeline = DataPreprocessingPipeline([
        ("column_cleaner", GenCleaner(null_threshold=0.5, columns_to_remove=["user"], column_for_deduplication="id")),
        ("column_cleaner", GenCleaner(null_threshold=0.05, columns_to_remove=["user"], column_for_deduplication="id")),
        ("flattener", DataFlattener())])
    processed_df = pipeline.transform(df)
    print("\nProcessed Data:")
    print(processed_df.head())
    return processed_df

def acc_process(df):
    pipeline = DataPreprocessingPipeline([
        ("flattener", DataFlattener()),
        ("column_cleaner", GenCleaner(null_threshold=0.05, columns_to_remove=["user"], column_for_deduplication="user_id")),
        ])
    processed_df = pipeline.transform(df)
    print("\nProcessed Data:")
    print(processed_df.head())
    return processed_df
def main():
    df = filered_df()
    print(df.head())

    processes = {
        # "tweets": tweet_process,
        "accounts": lambda df: acc_process(df[['user', 'created_at']])
    }

    for name, func in processes.items():
        processed_df = func(df)
        processed_df.to_csv(f"backend/mlops/data/processed/{name}.csv", index=False)

if __name__ == "__main__":
    main()