import csv
from database_house import DatabaseHandler
class SolarRadiationDatabaseHandler(DatabaseHandler):
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
        return rows

    def write_to_csv(self, rows: list[tuple], file_path: str) -> None:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalConsumption'])
            writer.writerows(rows)

if __name__ == "__main__":
    handler=SolarRadiationDatabaseHandler()
    handler.read_database("irise.sqlite3")
    data=handler.extract_solar_radiation_data()
    handler.write_to_csv(data, "CSVs/solar_radiation_data.csv")
    handler.close_connection()
