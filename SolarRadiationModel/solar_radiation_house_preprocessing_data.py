from calendar import c
import pandas as pd
from HouseModel.house_helper_file import HouseHelperFile
from HouseModel.house import House
from HouseModel.house_preprocessing_data import HousePreprocessingData
from typing import Final
from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse

class SolarRadiationHousePreprocessingData:
    def __init__(self) -> None:
        self.threshold: Final[float] = 0.95
        self.house_preprocessing = HousePreprocessingData()

    def _change_timing_for_solar_radiation_data(self, house: House, solar_radiation_house: SolarRadiationHouse) -> None:
        if house.house_id != solar_radiation_house.house_id:
            return

        helper_method = HouseHelperFile()
        starting_time, ending_time = helper_method.show_starting_time_and_ending_time(house)
        if starting_time and ending_time:
        
            starting_time = pd.to_datetime(starting_time)
            ending_time = pd.to_datetime(ending_time)
        
            solar_radiation_house.solar_radiation = {
                t: v for t, v in solar_radiation_house.solar_radiation.items()
                if starting_time <= pd.to_datetime(t) <= ending_time
        }

    def filtrate_solar_radiation_houses_by_number_of_values(self, solar_radiation_houses: list[SolarRadiationHouse], consumption_houses: list[House]) -> list[SolarRadiationHouse]:
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses :list[SolarRadiationHouse] = []
        for house in solar_radiation_houses:
            if house.house_id in consumption_dict:
                consumption_house = consumption_dict[house.house_id]
                if len(house.solar_radiation) >= self.threshold*len(consumption_house.consumption):
                    filtered_solar_radiation_houses.append(house)
                else:
                    print(f"House {house.house_id} has less than {self.threshold} values and will be removed.")
        return filtered_solar_radiation_houses

    def filtrate_solar_radiation_houses_having_zeros_for_a_period_of_time(self, solar_radiation_houses: list[SolarRadiationHouse], consumption_houses: list[House]) -> list[SolarRadiationHouse]:
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses : list[SolarRadiationHouse] = []
        
        for house in solar_radiation_houses:
            if house.house_id in consumption_dict:
                consumption_house = consumption_dict[house.house_id]
                zero_count = self.house_preprocessing.remove_houses_having_zero_for_a_period_of_time(consumption_house)
                if zero_count == 0:
                    filtered_solar_radiation_houses.append(house)
        return filtered_solar_radiation_houses

    def match_houses_ids_and_match_timestamps(self, solar_houses: list[SolarRadiationHouse], consumption_houses: list[House]) -> None:
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for solar_house in solar_houses:
            if solar_house.house_id in consumption_dict:
                consumption_house = consumption_dict[solar_house.house_id]
                self._change_timing_for_solar_radiation_data(consumption_house, solar_house)
            else:
                print(f"No matching consumption data for solar house {solar_house.house_id}")
