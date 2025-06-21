from housebuilder import HouseBuilder
from solar_radiation_house import SolarRadiationHouse
import csv
import pandas as pd
class SolarRadiationHouseBuilder(HouseBuilder) :
    def __init__(self):
        super().__init__()
    def build(self, csv_path):
        solar_radiation_houses = {}
        rows=super().open_csv_file(csv_path)

        for house_id, timestamp, value in rows:
            if house_id not in solar_radiation_houses:
                solar_radiation_houses[house_id] = SolarRadiationHouse(house_id)
            solar_radiation_houses[house_id].add_solar_radiation(timestamp, value)
        return list(solar_radiation_houses.values())
    def export_to_csv_solar_radiation(self, solar_radiation_houses, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalValue'])
            for house in solar_radiation_houses:
                for timestamp,value in house.solar_radiation.items():
                    writer.writerow([house.house_id, timestamp, value])
    
    def match_and_filter_solar_houses(self,solar_houses, consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for solar_house in solar_houses:
            if solar_house.house_id in consumption_dict:
                consumption_house = consumption_dict[solar_house.house_id]
                solar_house.change_timing_for_solar_radiation(consumption_house)
            else:
                print(f"No matching consumption data for solar house {solar_house.house_id}")
    
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
        
if __name__ == "__main__":
    house_builder = HouseBuilder()
    houses = house_builder.build('houses_after_filtering_and_matching_with_weather_data.csv')

    solar_radiation_house_builder = SolarRadiationHouseBuilder()
    solar_radiation_house = solar_radiation_house_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    print(f"Number of solar radiation houses: {len(solar_radiation_house)}")
    solar_radiation_house = solar_radiation_house_builder.filtrate_solar_radiation_by_number_of_values(solar_radiation_house,houses,0.95)
    print(f"Number of solar radiation houses after filtering: {len(solar_radiation_house)}")
    solar_radiation_house= solar_radiation_house_builder.filtrate_solar_radiation_having_zeros_for_a_period_of_time(solar_radiation_house, houses)
    print(f"Number of solar radiation houses after filtering zeros: {len(solar_radiation_house)}")
    solar_radiation_house_dict={house.house_id: house for house in solar_radiation_house}
    for house in houses:
        if house.house_id not in solar_radiation_house_dict:
            houses.remove(house)
    print(f"Number of houses after filtering: {len(houses)}")
    print(f"Number of solar radiation houses after filtering: {len(solar_radiation_house)}")
    solar_radiation_house_builder.export_to_csv_solar_radiation(solar_radiation_house, 'solar_radiation_after_resampling_and_matching_houses.csv')
    house_builder.export_to_csv(houses, 'houses_after_filtering_and_matching_with_weather_data.csv')