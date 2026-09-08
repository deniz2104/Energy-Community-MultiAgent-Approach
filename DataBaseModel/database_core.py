import time
import pandas as pd

from DataBaseModel.constants import RAW_TABLES_DIR, CONSUMPTION_DATA_DIR

class _LazyTableCache(dict):
    def __missing__(self, key: str) -> pd.DataFrame:
        table = pd.read_csv(RAW_TABLES_DIR / f"{key}.csv")
        self[key] = table
        return table

class DataHandler():
    _tables = _LazyTableCache()

    @property
    def tables(self) -> dict[str, pd.DataFrame]:
        return DataHandler._tables

    @staticmethod
    def convert_epochtime_to_timestamp(data: pd.DataFrame) -> pd.DataFrame:
        data = data.copy()
        data['Timestamp'] = data['Timestamp'].apply(lambda e: time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(e)))
        return data

    @staticmethod
    def export_to_csv(data: pd.DataFrame, file_name: str, file_path: str = str(CONSUMPTION_DATA_DIR)) -> None:
        data.to_csv(f"{file_path}/{file_name}", index=False)
