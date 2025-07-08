import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from house import House
class AppliancePreprocessingData():
    def __init__(self):
        pass

    def eliminate_days_after_a_year(self,appliance,house):
        starting_time,ending_time = house.show_starting_time_and_ending_time()
        new_dictionary={}

        starting_time = pd.to_datetime(starting_time)
        ending_time = pd.to_datetime(ending_time)

        for appliance_type,pairs in appliance.appliance_consumption.items():
            new_pairs=[]
            timestamps=[pair[0] for pair in pairs]
            datatime_timestamps=pd.to_datetime(timestamps)
            for i,(timestamp,value) in enumerate(pairs):
                if starting_time <= datatime_timestamps[i] <= ending_time:
                    new_pairs.append((timestamp, value))
            new_dictionary[appliance_type]=new_pairs
        appliance.appliance_consumption=new_dictionary    
        print(appliance.appliance_consumption)

    def count_zeros_in_consumption(self,appliance):
        return {appliance_type: sum(value == 0 for _, value in consumption) for appliance_type, consumption in appliance.appliance_consumption.items()}
    
    def eliminate_appliances_with_lot_of_zeros_consumption(self,appliance):
        appliances_with_enough_data = {appliance_type: consumption for appliance_type, consumption in appliance.appliance_consumption.items() if sum(value == 0 for _, value in consumption) < len(consumption)-len(consumption)//24}
        appliance.appliance_consumption = appliances_with_enough_data
    
    def eliminate_anomalies_in_my_data(self,appliance):
        new_consumption = {}

        for appliance_type, pairs in appliance.appliance_consumption.items():
            timestamps = [pair[0] for pair in pairs]
            values = [pair[1] for pair in pairs]
            
            temp_consumption = dict(zip(timestamps, values))
            
            temp_house = House(appliance.house_id)
            temp_house.consumption = temp_consumption
            temp_house.eliminate_anomalies_in_data()
            
            filtered_pairs = [(timestamp, value) for timestamp, value in temp_house.consumption.items()]
            
            if filtered_pairs:
                new_consumption[appliance_type] = filtered_pairs
        
        appliance.appliance_consumption = new_consumption
    

    def eliminate_appliance_with_five_days_of_no_consumption(self,appliance):
        new_consumption = {}

        for appliance_type, pairs in appliance.appliance_consumption.items():
            timestamps = [pair[0] for pair in pairs]
            values = [pair[1] for pair in pairs]
            
            temp_consumption = dict(zip(timestamps, values))
            
            temp_house = House(appliance.house_id)
            temp_house.consumption = temp_consumption
            
            if (temp_house.remove_houses_having_zero_for_a_period_of_time(is_appliance=True)==0):
                filtered_pairs = [(timestamp, value) for timestamp, value in temp_house.consumption.items()]
                new_consumption[appliance_type] = filtered_pairs        
        appliance.appliance_consumption = new_consumption

    def remove_appliances_with_zero_data(self, appliances):
        for appliance in appliances:
            self.eliminate_appliances_with_lot_of_zeros_consumption(appliance)
    
    def eliminate_anomalies_in_appliances(self, appliances):
        for appliance in appliances:
            self.eliminate_anomalies_in_my_data(appliance)

    def eliminate_appliances_with_five_days_of_no_consumption(self, appliances):
        for appliance in appliances:
            self.eliminate_appliance_with_five_days_of_no_consumption(appliance)

    def matching_timestamps_between_appliance_and_house(self, appliances,consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for appliance in appliances:
            if appliance.house_id in consumption_dict:
                consumption_house = consumption_dict[appliance.house_id]
                self.eliminate_days_after_a_year(appliance,consumption_house)