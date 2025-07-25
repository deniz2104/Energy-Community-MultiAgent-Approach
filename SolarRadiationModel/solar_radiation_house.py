from HouseModel.house import House
from HelperFiles.file_to_handle_absolute_path_imports import *

class SolarRadiationHouse(House):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.solar_radiation = {}
    def add_solar_radiation(self, timestamp, solar_radiation_data):
        self.solar_radiation[timestamp] = solar_radiation_data