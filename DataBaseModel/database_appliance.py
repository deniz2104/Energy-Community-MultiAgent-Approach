import time
import csv
from database_house import DatabaseHandler
from HelperFiles.file_to_get_house_ids import house_ids

class DatabaseHandlerAppliance(DatabaseHandler):
    def __init__(self):
        pass
    def read_database(self, database_path):
        super().read_database(database_path)
    def extract_data(self):
        self.cursor.execute("""
        SELECT DISTINCT
            h.ID,
            c.EpochTime,
            c.ApplianceIDREF,
            at.Name,
            c.TotalValue
        FROM House h
        JOIN(
            SELECT HouseIDREF, ApplianceIDREF, EpochTime, Value AS TotalValue
            FROM Consumption
            GROUP BY HouseIDREF, ApplianceIDREF, EpochTime
        ) c ON c.HouseIDREF = h.ID
        JOIN Appliance a ON a.ID = c.ApplianceIDREF
        JOIN ApplianceType at ON at.ID = a.TypeIDREF
        WHERE h.ID IN ({})
        ORDER BY h.ID;
        """.format(','.join(['?']*len(house_ids))), house_ids)
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
            writer.writerow(['HouseID', 'EpochTime','Appliance_ID','Appliance_Name','TotalValue'])
            writer.writerows(data)

    def close_connection(self):
        super().close_connection()

if __name__ == "__main__":
    db_handler = DatabaseHandlerAppliance()
    db_handler.read_database('irise.sqlite3')
    data = db_handler.extract_data()
    db_handler.write_to_csv(data, 'CSVs/appliance_consumption_data.csv')
    db_handler.close_connection()