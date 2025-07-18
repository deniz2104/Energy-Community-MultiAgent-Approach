import pandas as pd

class ApplianceConsumptionStatistics:
    def __init__(self):
        pass

    def get_mean_consumption_by_hour(self, appliance, dictionary_with_on_off_values, hours_distribution, 
                                   NIGHT_HOURS={0, 1, 2, 3, 4, 5, 6, 22, 23}, is_night=False):
        mean_consumption_by_hour = {}
        
        for appliance_type, consumption in appliance.appliance_consumption.items():
            target_hours = NIGHT_HOURS if is_night else {h for h in range(24) if h not in NIGHT_HOURS}
            hours = {hour: 0 for hour in target_hours}
            target_status = 0 if is_night else 1
            
            for timestamp, value in consumption:
                hour = pd.to_datetime(timestamp).hour
                if hour in target_hours and dictionary_with_on_off_values[appliance_type].get(timestamp) == target_status:
                    hours[hour] += value
            
            mean_consumption_by_hour[appliance_type] = {
                hour: count / hours_distribution[appliance_type].get(hour, 1) 
                for hour, count in hours.items()
            }
        
        return mean_consumption_by_hour