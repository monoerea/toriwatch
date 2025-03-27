import pandas as pd

def load_data(file_path: str, index_col: str ) -> pd.DataFrame:
    """Load data from a file based on the file extension.
    
    Supported formats: CSV, JSON, ZIP (CSV), XLSX, XLS, SQLite.
    
    :param file_path: Path to the data file.
    :return: DataFrame containing the data.
    """

    return pd.read_csv(file_path, index_col=index_col)

def data_inspection(df: pd.DataFrame) -> None:
    """Inspect the DataFrame for basic information.
    :param df: DataFrame to inspect.
    """
    print("Data Overview:")
    print(df.head())
    print("\nData Info:")
    print(df.info())
    print("\nData Description:")
    print(df.describe())

def main():
    """Main funtion for testing the code.
    """
    filepaths = {
        "backend/mlops/data/processed/accounts.csv": "user_id",
        "backend/mlops/data/processed/tweets.csv":"id"
    }
    for filepath, col in filepaths.items():
        df = load_data(filepath, col)
        data_inspection(df)

if __name__ == "__main__":
    main()