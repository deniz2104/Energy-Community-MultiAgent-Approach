from HouseModel.house import House
from HelperFiles.file_to_handle_absolute_path_imports import *

class SolarRadiationHouse(House):
    def __init__(self, house_id: int) -> None:
        super().__init__(house_id)
        self.solar_radiation: dict[str, float] = {}
        
    def add_solar_radiation(self, timestamp: str, solar_radiation_data: float) -> None:
        self.solar_radiation[timestamp] = solar_radiation_data