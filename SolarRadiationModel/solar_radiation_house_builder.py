from HouseModel.house_builder import HouseBuilder
from .solar_radiation_house import SolarRadiationHouse
from HelperFiles.file_to_handle_absolute_path_imports import *
import csv
class SolarRadiationHouseBuilder(HouseBuilder) :
    def __init__(self):
        super().__init__()
    def build(self, csv_path):
        solar_radiation_houses = {}
        rows=super().open_csv_file(csv_path)

        for house_id, timestamp, solar_radiation_consumption in rows:
            if house_id not in solar_radiation_houses:
                solar_radiation_houses[house_id] = SolarRadiationHouse(house_id)
            solar_radiation_houses[house_id].add_solar_radiation(timestamp, solar_radiation_consumption)
        return list(solar_radiation_houses.values())
    def export_to_csv_solar_radiation(self, solar_radiation_houses, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalValue'])
            for house in solar_radiation_houses:
                for timestamp, solar_radiation_consumption in house.solar_radiation.items():
                    writer.writerow([house.house_id, timestamp, solar_radiation_consumption])