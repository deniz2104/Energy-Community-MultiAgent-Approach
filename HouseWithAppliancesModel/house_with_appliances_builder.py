import csv
from .house_with_appliances import HouseWithAppliancesConsumption
from HelperFiles.file_to_handle_absolute_path_imports import *

class HouseWithAppliancesBuilder:
    def __init__(self):
        pass
    
    def _open_csv_file(self, csv_path):
        results=[]
        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                timestamp = row['EpochTime']
                appliance_name = row['Appliance_Name']
                consumption = float(row['TotalConsumption'])
                results.append((house_id, timestamp,appliance_name,consumption))
        return results

    def export_to_csv(self, appliances, file_path):
         with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime','Appliance_Name','TotalConsumption'])
            for appliance in appliances:
                for appliance_name,pairs in appliance.appliance_consumption.items():
                    for timestamp, consumption in pairs:
                        writer.writerow([appliance.house_id, timestamp,appliance_name,consumption])

    def build(self, csv_path):
        houses_with_appliances_consumption = {}
        rows=self._open_csv_file(csv_path)
        for house_id, timestamp, appliance_name, consumption in rows:
            if house_id not in houses_with_appliances_consumption:
                houses_with_appliances_consumption[house_id] = HouseWithAppliancesConsumption(house_id)

            houses_with_appliances_consumption[house_id].add_appliance_consumption(timestamp, appliance_name, consumption)
        return list(houses_with_appliances_consumption.values())