import csv
import time
from database_house import DatabaseHandler
class SolarRadiationDatabaseHandler(DatabaseHandler):

    def __init__(self):
        pass
    def read_database(self, database_path):
        super().read_database(database_path)
    def extract_solar_radiation_data(self):
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
        rows=list(rows)
        for i in range(len(rows)):
            row=list(rows[i])
            row[1]=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(row[1]))
            rows[i]=tuple(row)
        return rows
    
    def write_to_csv(self, data, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalSolarConsumption'])
            writer.writerows(data)
    
    def close_connection(self):
        super().close_connection()

if __name__ == "__main__":
    handler=SolarRadiationDatabaseHandler()
    handler.read_database("irise.sqlite3")
    data=handler.extract_solar_radiation_data()
    handler.write_to_csv(data, "CSVs/solar_radiation_data.csv")
    handler.close_connection()
