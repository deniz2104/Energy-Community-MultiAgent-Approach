from SolarRadiationModel.solar_radiation_house_builder import SolarRadiationHouseBuilder
from .power_estimated import PowerEstimator
from HelperFiles.file_to_handle_absolute_path_imports import *

class PowerEstimatedBuilder(SolarRadiationHouseBuilder):
    def __init__(self) -> None:
        pass
    def build(self,csv_path: str) -> list[PowerEstimator]:
        power_estimated_houses ={}
        rows=super().open_csv_file(csv_path)

        for house_id, timestamp, power_estimated in rows:
            if house_id not in power_estimated_houses:
                power_estimated_houses[house_id] = PowerEstimator(house_id)
            power_estimated_houses[house_id].add_consumption(timestamp,power_estimated)
            power_estimated_houses[house_id].add_power_estimated(timestamp, power_estimated)
        return list(power_estimated_houses.values())
    
    def determine_NEEG_for_all_houses(self, power_estimated_houses: list[PowerEstimator]) -> None:
        for house in power_estimated_houses:
            house.determine_NEEG()
