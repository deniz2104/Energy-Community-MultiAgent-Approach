import time
import csv
from database_house import DatabaseHandler
from HelperFiles.file_to_get_house_ids import house_ids

class DatabaseHandlerAppliance(DatabaseHandler):
    def __init__(self) -> None:
        pass
    def read_database(self, database_path: str) -> None:
        super().read_database(database_path)
    def extract_data(self) -> list[tuple]:
        self.cursor.execute("""
        SELECT DISTINCT
            h.ID,
            c.EpochTime,
            c.ApplianceIDREF,
            at.Name,
            c.TotalConsumption
        FROM House h
        JOIN(
            SELECT HouseIDREF, ApplianceIDREF, EpochTime, Value AS TotalConsumption
            FROM Consumption
            GROUP BY HouseIDREF, ApplianceIDREF, EpochTime
        ) c ON c.HouseIDREF = h.ID
        JOIN Appliance a ON a.ID = c.ApplianceIDREF
        JOIN ApplianceType at ON at.ID = a.TypeIDREF
        WHERE h.ID IN ({})
        ORDER BY h.ID;
        """.format(','.join(['?']*len(house_ids))), house_ids)
        rows = self.cursor.fetchall()
        return super().convert_rows_to_correct_format(rows)

    def write_to_csv(self, data: list[tuple], file_path: str) -> None:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime','Appliance_ID','Appliance_Name','TotalConsumption'])
            writer.writerows(data)

    def close_connection(self) -> None:
        super().close_connection()

if __name__ == "__main__":
    db_handler = DatabaseHandlerAppliance()
    db_handler.read_database('irise.sqlite3')
    data = db_handler.extract_data()
    db_handler.write_to_csv(data, 'CSVs/appliance_consumption_data.csv')
    db_handler.close_connection()