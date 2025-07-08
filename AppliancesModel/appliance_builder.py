import csv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .appliance import Appliance

class ApplianceBuilder:
    def __init__(self):
        pass
    
    def open_csv_file(self, csv_path):
        results=[]
        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                timestamp = row['EpochTime']
                appliance_name = row['Appliance_Name']
                value = float(row['TotalValue'])
                results.append((house_id, timestamp,appliance_name,value))
        return results

    def export_to_csv(self, appliances, file_path):
         with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime','Appliance_Name','TotalValue'])
            for appliance in appliances:
                for appliance_name,pairs in appliance.appliance_consumption.items():
                    for timestamp, value in pairs:
                        writer.writerow([appliance.house_id, timestamp,appliance_name,value])

    def build(self, csv_path):
        appliances ={}
        rows=self.open_csv_file(csv_path)
        for house_id, timestamp, appliance_name, value in rows:
            if house_id not in appliances:
                appliances[house_id] = Appliance(house_id)

            appliances[house_id].add_appliance_consumption(timestamp, appliance_name, value)
        return list(appliances.values())