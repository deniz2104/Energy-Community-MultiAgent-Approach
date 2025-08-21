import pandas as pd
from HouseModel.house import House
from HouseModel.house_helper_file import HouseHelperFile
from HouseModel.house_preprocessing_data import HousePreprocessingData
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption

class HouseWithAppliancesPreprocessingData:
    def __init__(self) -> None:
        pass

    def eliminate_days_after_a_year(self, house_with_appliances: HouseWithAppliancesConsumption, house: House) -> None:
        helper_method = HouseHelperFile()
        starting_time, ending_time = helper_method.show_starting_time_and_ending_time(house)
        new_dictionary: dict[str, dict[str, float]] = {}
        
        starting_time = pd.to_datetime(starting_time)
        ending_time = pd.to_datetime(ending_time)

        for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
            new_consumption: dict[str, float] = {}
            timestamps = list(consumption.keys())
            datetime_timestamps = pd.to_datetime(timestamps)
            for i, (timestamp, value) in enumerate(consumption.items()):
                if starting_time <= datetime_timestamps[i] <= ending_time:
                    new_consumption[timestamp] = value
            new_dictionary[appliance_type] = new_consumption
        house_with_appliances.appliance_consumption=new_dictionary    

    def eliminate_appliances_with_lot_of_zeros_consumption(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        appliances_with_enough_data = {appliance_type: consumption for appliance_type, consumption in house_with_appliances.appliance_consumption.items() if sum(value == 0 for _, value in consumption.items()) < len(consumption)-len(consumption)//24}
        house_with_appliances.appliance_consumption = appliances_with_enough_data

    def eliminate_anomalies_in_my_data(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        new_consumption :dict[str, dict[str, float]] = {}
        house_preprocessing = HousePreprocessingData()

        for appliance_type, consumption in house_with_appliances.appliance_consumption.items():

            temp_house = House(house_with_appliances.house_id)
            temp_house.consumption = consumption
            house_preprocessing.eliminate_anomalies_in_data(temp_house)

            filtered_consumption= dict(temp_house.consumption.items())

            if filtered_consumption:
                new_consumption[appliance_type] = filtered_consumption

        house_with_appliances.appliance_consumption = new_consumption

    def eliminate_appliance_with_five_days_of_no_consumption(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        new_consumption :dict[str, dict[str, float]] = {}
        house_preprocessing = HousePreprocessingData()

        for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
            temp_house = House(house_with_appliances.house_id)
            temp_house.consumption = consumption
            
            if (house_preprocessing.remove_houses_having_zero_for_a_period_of_time(temp_house, is_appliance=True)==0):
                filtered_consumption = dict(temp_house.consumption.items())
                new_consumption[appliance_type] = filtered_consumption
        house_with_appliances.appliance_consumption = new_consumption