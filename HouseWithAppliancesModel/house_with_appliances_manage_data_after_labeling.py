from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import NIGHT_HOURS,TOTAL_HOURS
from .house_with_appliances_label_for_on_and_off_values import HouseWithAppliancesOnOffValues
import pandas as pd
import numpy as np

class HouseWithAppliancesManageDataAfterLabeling:
    def __init__(self) -> None:
        self.helper_class: HouseWithAppliancesOnOffValues = HouseWithAppliancesOnOffValues()
    def count_on_off_values_per_time_period(self,dictionary_with_on_off_values:dict[str, dict[int, int]]) -> dict[str, dict[int, int]]:
        hour_dictionary: dict[str, dict[int, int]] = {}
        for appliance_type, pairs in dictionary_with_on_off_values.items():
            hours_count= {hour: 0 for hour in range(TOTAL_HOURS)}
            
            for timestamp, state in pairs.items():
                hour = pd.to_datetime(timestamp).hour
                
                if (hour in NIGHT_HOURS and state == 0) or (hour not in NIGHT_HOURS and state == 1):
                    hours_count[hour] += 1
            hour_dictionary[appliance_type] = {hour: count for hour, count in hours_count.items() if count > 0}
        return hour_dictionary

    def count_off_values_per_appliance(self, dictionary_with_on_off_values: dict[str, dict[int, int]]) -> dict[str, int]:
        off_values_count: dict[str, int] = {}
        for appliance_type, pairs in dictionary_with_on_off_values.items():
            off_count = sum(1 for _, state in pairs.items() if state == 0)
            off_values_count[appliance_type] = off_count
        return off_values_count
    
    def gather_off_values_per_appliance(self, house_with_appliances: dict[str, dict[str, float]]) -> dict[str, np.ndarray[int]]:
        off_values_per_appliance: dict[str, np.ndarray[int]] = {}
        for appliance_type, pairs in house_with_appliances.appliance_consumption.items():
            values : list[float] = []
            consumption_values = np.array(np.trim_zeros(list(pairs.values()))).reshape(-1, 1)
            scaler, kmeans, centroids = self.helper_class.cluster_data(consumption_values)

            off_label = np.argmin(centroids)

            values.extend(self.helper_class.filter_by_cluster(list(pairs.items()), kmeans, scaler, off_label))
            off_values_per_appliance[appliance_type] = np.unique([pair[1] for pair in values])
        return off_values_per_appliance 
        