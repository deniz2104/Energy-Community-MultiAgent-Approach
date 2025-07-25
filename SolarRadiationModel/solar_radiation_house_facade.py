from typing import Optional
from HouseModel.house_builder import HouseBuilder
from HouseModel.house import House
from .solar_radiation_house_builder import SolarRadiationHouseBuilder
from .solar_radiation_house_preprocessing_data import SolarRadiationHousePreprocessingData
from .solar_radiation_plotter import SolarRadiationPLotter
from .solar_radiation_house import SolarRadiationHouse
from HelperFiles.file_to_handle_absolute_path_imports import *

class SolarRadiationHouseFacade:
    def __init__(self) -> None:
        self.builder: SolarRadiationHouseBuilder = SolarRadiationHouseBuilder()
        self.preprocessor: SolarRadiationHousePreprocessingData = SolarRadiationHousePreprocessingData()
        self.house_builder: HouseBuilder = HouseBuilder()
        self.plotter: SolarRadiationPLotter = SolarRadiationPLotter()

    def build_solar_radiation_data(self, csv_path: str) -> list[SolarRadiationHouse]:
        return self.builder.build(csv_path)

    def process_solar_radiation_pipeline(self, csv_path: str, houses: list[House], export_solar_radiation_path: Optional[str] = None, export_house_path: Optional[str] = None) -> list[SolarRadiationHouse]:
        solar_radiation_houses = self.build_solar_radiation_data(csv_path)

        self.preprocessor.match_houses_ids_and_match_timestamps(solar_radiation_houses, houses)

        solar_radiation_houses = self.preprocessor.filtrate_solar_radiation_houses_having_zeros_for_a_period_of_time(solar_radiation_houses, houses)

        solar_radiation_houses = self.preprocessor.filtrate_solar_radiation_houses_by_number_of_values(solar_radiation_houses, houses)

        solar_radiation_house_dict = {house.house_id: house for house in solar_radiation_houses}
        houses_to_remove = []
        for house in houses:
            if house.house_id not in solar_radiation_house_dict:
                houses_to_remove.append(house)
        
        for house in houses_to_remove:
            houses.remove(house)

        if export_solar_radiation_path:
            self.builder.export_to_csv(solar_radiation_houses, export_solar_radiation_path)

        if export_house_path:
            self.house_builder.export_to_csv(houses, export_house_path)

        return solar_radiation_houses

    def plot_solar_radiation_data(self, solar_radiation_house: SolarRadiationHouse) -> None:
        self.plotter.plot_solar_radiation_over_time(solar_radiation_house)