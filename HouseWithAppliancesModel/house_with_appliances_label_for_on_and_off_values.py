from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from .house_with_appliances import HouseWithAppliancesConsumption
from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import NIGHT_HOURS,TOTAL_HOURS

class HouseWithAppliancesOnOffValues:
    def __init__(self):
        self.random_state = 42 
        self.chunk_size = 168
        self.number_of_clusters = 2

    def _cluster_data(self,data_for_kmeans : np.ndarray) -> tuple[StandardScaler, KMeans, np.ndarray]:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_for_kmeans)

        kmeans = KMeans(n_clusters=self.number_of_clusters, random_state=self.random_state, n_init=50)
        kmeans.fit_predict(scaled_data)

        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler,kmeans,centroids

    def _filter_by_cluster(self,chunk:np.ndarray,kmeans:KMeans,scaler:StandardScaler,label:int) -> list[tuple[str, float]]:
        return [data_point for data_point in chunk if kmeans.predict(scaler.transform([[data_point[1]]]))[0] == label]

    def determine_on_off_periods(self,house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[int, int]]:
        dictionary_with_on_off_values = {}
        for appliance_type, pairs in house_with_appliances.appliance_consumption.items():
            off_pairs, on_pairs = [], []
            
            for i in range(0, len(pairs), self.chunk_size):
                chunk = list(set(pairs[i:i+self.chunk_size]))
                consumption_values = np.array([pair[1] for pair in chunk]).reshape(-1, 1)
                scaler, kmeans, centroids = self._cluster_data(consumption_values)

                off_label = np.argmin(centroids)
                on_label = np.argmax(centroids)

                off_pairs.extend(self._filter_by_cluster(chunk, kmeans, scaler, off_label))
                on_pairs.extend(self._filter_by_cluster(chunk, kmeans, scaler, on_label))

            labeled = [(timestamp, 0) for timestamp, _ in off_pairs] + [(timestamp, 1) for timestamp, _ in on_pairs]
            dictionary_with_on_off_values[appliance_type] = labeled
        return dictionary_with_on_off_values

    def count_on_off_values_per_time_period(self,dictionary_with_on_off_values:dict[str, dict[int, int]]) -> dict[str, dict[int, int]]:
        hour_dictionary ={}
        for appliance_type, pairs in dictionary_with_on_off_values.items():
            hours_count= {hour: 0 for hour in range(TOTAL_HOURS)}
            
            for timestamp, state in pairs:
                hour = pd.to_datetime(timestamp).hour
                
                if (hour in NIGHT_HOURS and state == 0) or (hour not in NIGHT_HOURS and state == 1):
                    hours_count[hour] += 1
            hour_dictionary[appliance_type] = {hour: count for hour, count in hours_count.items() if count > 0}
        return hour_dictionary