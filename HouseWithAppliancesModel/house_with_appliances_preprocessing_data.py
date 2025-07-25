import pandas as pd
from HouseModel.house import House
from HouseModel.house_helper_file import HouseHelperFile
from .house_with_appliances import HouseWithAppliancesConsumption
from HelperFiles.file_to_handle_absolute_path_imports import *

class HouseWithAppliancesPreprocessingData:
    def __init__(self) -> None:
        pass

    def _eliminate_days_after_a_year(self, house_with_appliances: HouseWithAppliancesConsumption, house: House) -> None:
        helper_method = HouseHelperFile()
        starting_time, ending_time = helper_method.show_starting_time_and_ending_time(house)
        new_dictionary: dict[str, list[tuple[str, float]]] = {}

        starting_time = pd.to_datetime(starting_time)
        ending_time = pd.to_datetime(ending_time)

        for appliance_type, pairs in house_with_appliances.appliance_consumption.items():
            new_pairs: list[tuple[str, float]] = []
            timestamps = [pair[0] for pair in pairs]
            datatime_timestamps=pd.to_datetime(timestamps)
            for i,(timestamp,value) in enumerate(pairs):
                if starting_time <= datatime_timestamps[i] <= ending_time:
                    new_pairs.append((timestamp, value))
            new_dictionary[appliance_type]=new_pairs
        house_with_appliances.appliance_consumption=new_dictionary    

    def _count_zeros_in_consumption(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, int]:
        return {appliance_type: sum(value == 0 for _, value in consumption) for appliance_type, consumption in house_with_appliances.appliance_consumption.items()}

    def _eliminate_appliances_with_lot_of_zeros_consumption(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        appliances_with_enough_data = {appliance_type: consumption for appliance_type, consumption in house_with_appliances.appliance_consumption.items() if sum(value == 0 for _, value in consumption) < len(consumption)-len(consumption)//24}
        house_with_appliances.appliance_consumption = appliances_with_enough_data

    def _eliminate_anomalies_in_my_data(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        new_consumption = {}

        for appliance_type, pairs in house_with_appliances.appliance_consumption.items():
            timestamps = [pair[0] for pair in pairs]
            values = [pair[1] for pair in pairs]
            
            temp_consumption = dict(zip(timestamps, values))

            temp_house = House(house_with_appliances.house_id)
            temp_house.consumption = temp_consumption
            temp_house.eliminate_anomalies_in_data()
            
            filtered_pairs = [(timestamp, value) for timestamp, value in temp_house.consumption.items()]
            
            if filtered_pairs:
                new_consumption[appliance_type] = filtered_pairs

        house_with_appliances.appliance_consumption = new_consumption

    def _eliminate_appliance_with_five_days_of_no_consumption(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        new_consumption = {}

        for appliance_type, pairs in house_with_appliances.appliance_consumption.items():
            timestamps = [pair[0] for pair in pairs]
            values = [pair[1] for pair in pairs]
            
            temp_consumption = dict(zip(timestamps, values))

            temp_house = House(house_with_appliances.house_id)
            temp_house.consumption = temp_consumption
            
            if (temp_house.remove_houses_having_zero_for_a_period_of_time(is_appliance=True)==0):
                filtered_pairs = [(timestamp, value) for timestamp, value in temp_house.consumption.items()]
                new_consumption[appliance_type] = filtered_pairs        
        house_with_appliances.appliance_consumption = new_consumption

    def remove_appliances_with_zero_data(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> None:
        for house in houses_with_appliances:
            self._eliminate_appliances_with_lot_of_zeros_consumption(house)

    def eliminate_anomalies_in_appliances(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> None:
        for house in houses_with_appliances:
            self._eliminate_anomalies_in_my_data(house)

    def eliminate_appliances_with_five_days_of_no_consumption(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> None:
        for house in houses_with_appliances:
            self._eliminate_appliance_with_five_days_of_no_consumption(house)

    def matching_timestamps_between_appliance_and_house(self, house_with_appliances: list[HouseWithAppliancesConsumption], consumption_houses: list[House]) -> None:
        consumption_dict = {house.house_id: house for house in consumption_houses}

        for house in house_with_appliances:
            if house.house_id in consumption_dict:
                consumption_house = consumption_dict[house.house_id]
                self._eliminate_days_after_a_year(house, consumption_house)