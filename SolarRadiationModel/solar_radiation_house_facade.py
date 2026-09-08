from typing import Optional
from HouseModel.house import House
from SolarRadiationModel.solar_radiation_house_preprocessing_data import SolarRadiationHousePreprocessingData
from SolarRadiationModel.solar_radiation_plotter import SolarRadiationPlotter
from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse
from CsvModel.csv_core import export_to_csv

class SolarRadiationHouseFacade:
    def __init__(self) -> None:
        self.preprocessor = SolarRadiationHousePreprocessingData()
        self.plotter = SolarRadiationPlotter()

    def build_solar_radiation_data(self, csv_path: str) -> list[SolarRadiationHouse]:
        return SolarRadiationHouse.build(csv_path)

    def process_solar_radiation_pipeline(self, csv_path: str, houses: list[House], export_solar_radiation_path: Optional[str] = None, export_house_path: Optional[str] = None) -> list[SolarRadiationHouse]:
        solar_radiation_houses = self.build_solar_radiation_data(csv_path)

        self.preprocessor.match_houses_ids_and_match_timestamps(solar_radiation_houses, houses)

        solar_radiation_houses = self.preprocessor.filtrate_solar_radiation_houses_having_zeros_for_a_period_of_time(solar_radiation_houses, houses)

        solar_radiation_houses = self.preprocessor.filtrate_solar_radiation_houses_by_number_of_values(solar_radiation_houses, houses)

        solar_radiation_house_dict = {house.house_id: house for house in solar_radiation_houses}
        
        houses_to_remove : list[House] = []
        for house in houses:
            if house.house_id not in solar_radiation_house_dict:
                houses_to_remove.append(house)
        
        for house in houses_to_remove:
            houses.remove(house)

        if export_solar_radiation_path:
            solar_radiation_rows = [(house.house_id, timestamp, value) for house in solar_radiation_houses for timestamp, value in house.solar_radiation.items()]
            export_to_csv(solar_radiation_rows, export_solar_radiation_path)

        if export_house_path:
            house_rows = [(house.house_id, timestamp, consumption) for house in houses for timestamp, consumption in house.consumption.items()]
            export_to_csv(house_rows, export_house_path)

        return solar_radiation_houses

    def plot_solar_radiation_data(self, solar_radiation_house: SolarRadiationHouse) -> None:
        self.plotter.plot_solar_radiation_over_time(solar_radiation_house)