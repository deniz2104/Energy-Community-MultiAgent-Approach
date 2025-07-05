import sqlite3
import time
import csv

class DatabaseHandler():
    def __init__(self):
        pass
    def read_database(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
    def extract_data(self):
        self.cursor.execute("""
            SELECT h.ID, cs.EpochTime, cs.TotalValue
            FROM House h
            JOIN (
                SELECT HouseIDREF, EpochTime, SUM(Value) AS TotalValue
                FROM Consumption
                GROUP BY HouseIDREF, EpochTime
            ) cs ON cs.HouseIDREF = h.ID
            ORDER BY h.ID;
        """)
        rows = self.cursor.fetchall()
        rows=list(rows)
        for i in range(len(rows)):
            row=list(rows[i])
            row[1]=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(row[1]))
            rows[i]=tuple(row)
        return rows

    def write_to_csv(self, data, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalValue'])
            writer.writerows(data)

    def close_connection(self):
        self.connection.close()
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    db_handler.read_database('irise.sqlite3')
    data = db_handler.extract_data()
    db_handler.write_to_csv(data,'consumption_data.csv')
    db_handler.close_connection()