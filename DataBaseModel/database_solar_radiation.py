import csv
import time
from database_house import DatabaseHandler
class SolarRadiationDatabaseHandler(DatabaseHandler):

    def __init__(self) -> None:
        pass
    def read_database(self, database_path: str) -> None:
        super().read_database(database_path)
    def extract_solar_radiation_data(self) -> list[tuple]:
        self.cursor.execute("""
            SELECT h.ID,WD.EpochTime, WD.TotalSolarConsumption
            FROM House h
            JOIN (
                SELECT WeatherStationIDREF, EpochTime, Value as TotalSolarConsumption
                FROM WeatherData
                WHERE WeatherVariableIDREF=4
                GROUP BY WeatherStationIDREF, EpochTime
                ORDER BY WeatherVariableIDREF DESC
            ) WD ON h.WeatherStationIDREF = WD.WeatherStationIDREF
            ORDER BY h.ID;
        """)
        rows= self.cursor.fetchall()
        return super().convert_rows_to_correct_format(rows)

    def write_to_csv(self, data: list[tuple], file_path: str) -> None:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalConsumption'])
            writer.writerows(data)

    def close_connection(self) -> None:
        super().close_connection()

if __name__ == "__main__":
    handler=SolarRadiationDatabaseHandler()
    handler.read_database("irise.sqlite3")
    data=handler.extract_solar_radiation_data()
    handler.write_to_csv(data, "CSVs/solar_radiation_data.csv")
    handler.close_connection()
