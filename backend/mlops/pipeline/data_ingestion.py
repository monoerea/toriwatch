import os
import pandas as pd
import logging
import sqlite3
from abc import ABC, abstractmethod
from zipfile import ZipFile
from typing import List
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "backend", "mlops", "data", "raw")

os.makedirs(RAW_DATA_DIR, exist_ok=True)

class DataIngestor(ABC):
    """Abstract base class for data ingestion."""

    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        """Ingest data from a file and return a DataFrame."""
        pass

    def _save_dataframe(self, df: pd.DataFrame, file_name: str) -> pd.DataFrame:
        """Save DataFrame to CSV and return it."""
        save_path = os.path.join(RAW_DATA_DIR, file_name)
        df.to_csv(save_path, index=False)
        logging.info(f"Data saved to {save_path}")
        return df


# ======= CSV =======
class CSVDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        return self._save_dataframe(df, "ingested_csv_data.csv")


# ======= JSON =======
class JSONDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        df = pd.read_json(file_path, orient='records')
        return self._save_dataframe(df, "ingested_json_data.csv")


# ======= ZIP (Handles CSV & JSON inside) =======
class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        extracted_files = self._extract_zip(file_path)
        data_files = [os.path.join(RAW_DATA_DIR, f) for f in extracted_files if f.endswith(('.csv', '.json'))]

        if not data_files:
            raise ValueError("No CSV or JSON files found in the ZIP archive.")

        merged_df = self._merge_files(data_files)
        return self._save_dataframe(merged_df, "merged_zip_data.csv")

    def _extract_zip(self, file_path: str) -> List[str]:
        with ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(RAW_DATA_DIR)
        return os.listdir(RAW_DATA_DIR)

    def _merge_files(self, files: List[str]) -> pd.DataFrame:
        df_list = []
        _, first_df = self._read_file(files[0])
        df_list.append(first_df)

        for file_path in files[1:]:
            _, df = self._read_file(file_path)
            if list(df.columns) == list(first_df.columns):
                df_list.append(df)
            else:
                logging.warning(f"Skipping {file_path} due to mismatched structure.")

        return pd.concat(df_list, ignore_index=True) if len(df_list) > 1 else first_df

    def _read_file(self, file_path: str) -> tuple:
        if file_path.endswith('.csv'):
            return file_path, pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            return file_path, pd.read_json(file_path, orient='records')
        else:
            raise ValueError(f"Unsupported file format: {file_path}")


# ======= Excel (XLSX, XLS) =======
class ExcelDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        return self._save_dataframe(df, "ingested_excel_data.csv")

# ======= SQLite Database =======
class SQLiteDataIngestor(DataIngestor):
    def __init__(self, table_name: str):
        """Initialize table name for reading data from SQLite."""
        self.table_name = table_name

    def ingest(self, file_path: str) -> pd.DataFrame:
        """Read from a local SQLite database."""
        if not file_path.endswith(".sqlite") and not file_path.endswith(".db"):
            raise ValueError("Invalid SQLite database file.")

        conn = sqlite3.connect(file_path)
        df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)
        conn.close()

        return self._save_dataframe(df, "ingested_sqlite_data.csv")
# ======= Factory =======
class DataIngestorFactory:
    @staticmethod
    def get_ingestor(file_path: str) -> DataIngestor:
        if file_path.endswith('.csv'):
            return CSVDataIngestor()
        elif file_path.endswith('.json'):
            return JSONDataIngestor()
        elif file_path.endswith('.zip'):
            return ZipDataIngestor()
        elif file_path.endswith(('.xls', '.xlsx')):
            return ExcelDataIngestor()
        elif file_path.endswith(('.sqlite', '.db')):
            return SQLiteDataIngestor(table_name="users")
        else:
            raise ValueError("Unsupported file format.")

# ======= Example Usage =======
def main():
    ingestors = [
        CSVDataIngestor(),
        JSONDataIngestor(),
        ZipDataIngestor(),
        ExcelDataIngestor(),
        # DataIngestor(db_url="sqlite:///my_database.db", table_name="users"),
    ]

    test_files = [
        "sample.csv",
        "sample.json",
        "sample.zip",
        "sample.xlsx",
        "my_database.sqlite"
    ]

    for ingestor, file in zip(ingestors, test_files):
        try:
            df = ingestor.ingest(file)
            print(f"Ingested {file}: {df.shape}")
        except Exception as e:
            logging.error(f"Error processing {file}: {e}")


if __name__ == "__main__":
    #main()
    pass