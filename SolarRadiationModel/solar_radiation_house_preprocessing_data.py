import pandas as pd
class SolarRadiationHousePreprocessingData:
    def change_timing_for_solar_radiation(self, house):
        if house.house_id != self.house_id:
            return
    
        starting_time, ending_time = house.show_starting_time_and_ending_time()
        if starting_time and ending_time:
        
            starting_time = pd.to_datetime(starting_time)
            ending_time = pd.to_datetime(ending_time)
        
            self.solar_radiation = {
                t: v for t, v in self.solar_radiation.items()
                if starting_time <= pd.to_datetime(t) <= ending_time
        }
        
    def filtrate_solar_radiation_by_number_of_values(self, solar_radiation_houses,consumption_houses, threshold=0.95):
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses = []
        for house in solar_radiation_houses:
            if house.house_id in consumption_dict:
                consumption_house = consumption_dict[house.house_id]
                if len(house.solar_radiation) >= threshold*len(consumption_house.consumption):
                    filtered_solar_radiation_houses.append(house)
                else:
                    print(f"House {house.house_id} has less than {threshold} values and will be removed.")
        return filtered_solar_radiation_houses
    
    def filtrate_solar_radiation_having_zeros_for_a_period_of_time(self, solar_radiation_houses, consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses = []
        
        for house in solar_radiation_houses:
            if house.house_id in consumption_dict:
                house.consumption = house.solar_radiation.copy()
                zero_count= house.remove_houses_having_zero_for_a_period_of_time()
                if zero_count == 0:
                    filtered_solar_radiation_houses.append(house)
        return filtered_solar_radiation_houses
    
    def match_and_filter_solar_houses(self,solar_houses, consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for solar_house in solar_houses:
            if solar_house.house_id in consumption_dict:
                consumption_house = consumption_dict[solar_house.house_id]
                self.change_timing_for_solar_radiation(consumption_house)
            else:
                print(f"No matching consumption data for solar house {solar_house.house_id}")
