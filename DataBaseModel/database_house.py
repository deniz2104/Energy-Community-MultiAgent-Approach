import sqlite3
import time
import csv

class DatabaseHandler():
    def __init__(self) -> None:
        pass
    def read_database(self, database_path: str) -> None:
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
    def extract_data(self) -> list[tuple]:
        self.cursor.execute("""
            SELECT h.ID, cs.EpochTime, cs.TotalConsumption
            FROM House h
            JOIN (
                SELECT HouseIDREF, EpochTime, SUM(Value) AS TotalConsumption
                FROM Consumption
                GROUP BY HouseIDREF, EpochTime
            ) cs ON cs.HouseIDREF = h.ID
            ORDER BY h.ID;
        """)
        rows = self.cursor.fetchall()
        return self._convert_rows_to_correct_format(rows)

    def convert_rows_to_correct_format(self, rows: list[tuple]) -> list[tuple]:
        rows = list(rows)
        for i in range(len(rows)):
            row=list(rows[i])
            row[1]=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(row[1]))
            rows[i]=tuple(row)
        return rows

    def write_to_csv(self, data: list[tuple], file_path: str) -> None:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalConsumption'])
            writer.writerows(data)

    def close_connection(self) -> None:
        self.connection.close()
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    db_handler.read_database('irise.sqlite3')
    data = db_handler.extract_data()
    db_handler.write_to_csv(data,'CSVs/consumption_data.csv')
    db_handler.close_connection()