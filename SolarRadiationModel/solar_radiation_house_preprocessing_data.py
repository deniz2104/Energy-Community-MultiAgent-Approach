import pandas as pd
from HouseModel.house_helper_file import HouseHelperFile
class SolarRadiationHousePreprocessingData:
    def __init__(self):
        self.threshold = 0.95
    def _change_timing_for_solar_radiation_data(self, house):
        if house.house_id != self.house_id:
            return

        helper_method=HouseHelperFile()
        starting_time, ending_time = helper_method.show_starting_time_and_ending_time(house)
        if starting_time and ending_time:
        
            starting_time = pd.to_datetime(starting_time)
            ending_time = pd.to_datetime(ending_time)
        
            self.solar_radiation = {
                t: v for t, v in self.solar_radiation.items()
                if starting_time <= pd.to_datetime(t) <= ending_time
        }
        
    def filtrate_solar_radiation_houses_by_number_of_values(self, solar_radiation_houses,consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses = []
        for house in solar_radiation_houses:
            if house.house_id in consumption_dict:
                consumption_house = consumption_dict[house.house_id]
                if len(house.solar_radiation) >= self.threshold*len(consumption_house.consumption):
                    filtered_solar_radiation_houses.append(house)
                else:
                    print(f"House {house.house_id} has less than {self.threshold} values and will be removed.")
        return filtered_solar_radiation_houses
    
    def filtrate_solar_radiation_houses_having_zeros_for_a_period_of_time(self, solar_radiation_houses, consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses = []
        
        for house in solar_radiation_houses:
            if house.house_id in consumption_dict:
                house.consumption = house.solar_radiation.copy()
                zero_count= house.remove_houses_having_zero_for_a_period_of_time()
                if zero_count == 0:
                    filtered_solar_radiation_houses.append(house)
        return filtered_solar_radiation_houses
    
    def match_houses_ids_and_match_timestamps(self,solar_houses, consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for solar_house in solar_houses:
            if solar_house.house_id in consumption_dict:
                consumption_house = consumption_dict[solar_house.house_id]
                self._change_timing_for_solar_radiation_data(consumption_house)
            else:
                print(f"No matching consumption data for solar house {solar_house.house_id}")
