import pandas as pd
from HelperFiles.hours_for_day_and_night import NIGHT_HOURS,TOTAL_HOURS

class HouseWithAppliancesStatistics:
    def __init__(self):
        self.period = 365

    def get_mean_consumption_by_hour(self, houses_with_appliances, dictionary_with_on_off_values, hours_distribution, is_night=False):
        mean_consumption_by_hour = {}

        for appliance_type, consumption in houses_with_appliances.appliance_consumption.items():
            target_hours = NIGHT_HOURS if is_night else {h for h in range(TOTAL_HOURS) if h not in NIGHT_HOURS}
            on_off_values_per_appliance = dict(dictionary_with_on_off_values[appliance_type])
            hours = {hour: 0 for hour in target_hours}
            target_status = 0 if is_night else 1
            
            for timestamp, value in consumption:
                hour = pd.to_datetime(timestamp).hour
                if hour in target_hours and on_off_values_per_appliance.get(timestamp) == target_status:
                    hours[hour] += value
            
            mean_consumption_by_hour[appliance_type] = {
                hour: count / hours_distribution[appliance_type].get(hour, 1) 
                for hour, count in hours.items()
            }
        
        return mean_consumption_by_hour

    def determine_hours_weights(self,hour_dictionary):
        hours_weights = {}
        for appliance_type, hours in hour_dictionary.items():
            hours_weights[appliance_type] = {}
            for hour,count in hours.items():
                hours_weights[appliance_type][hour] = round(count / self.period, 2)
        return hours_weights