from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import NIGHT_HOURS,TOTAL_HOURS

class ApplianceOnOffValues:
    def __init__(self):
        self.random_state = 42 
        self.chunk_size = 168
        self.number_of_clusters = 2

    def _cluster_data(self,data_for_kmeans):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_for_kmeans)

        kmeans = KMeans(n_clusters=self.number_of_clusters, random_state=self.random_state, n_init=50)
        kmeans.fit_predict(scaled_data)

        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler,kmeans,centroids
            
    def _filter_by_cluster(self,chunk,kmeans,scaler,label): return [data_point for data_point in chunk if kmeans.predict(scaler.transform([[data_point[1]]]))[0] == label]
    def determine_on_off_periods(self,appliance,chunk_size=168):
        dictionary_with_on_off_values = {}
        for appliance_type, pairs in appliance.appliance_consumption.items():
            off_pairs, on_pairs = [], []
            
            for i in range(0, len(pairs), chunk_size):
                chunk = list(set(pairs[i:i+chunk_size]))
                consumption_values = np.array([pair[1] for pair in chunk]).reshape(-1, 1)
                scaler, kmeans, centroids = self._cluster_data(consumption_values)

                off_label = np.argmin(centroids)
                on_label = np.argmax(centroids)

                off_pairs.extend(self._filter_by_cluster(chunk, kmeans, scaler, off_label))
                on_pairs.extend(self._filter_by_cluster(chunk, kmeans, scaler, on_label))

            labeled = [(ts, 0) for ts, _ in off_pairs] + [(ts, 1) for ts, _ in on_pairs]
            dictionary_with_on_off_values[appliance_type] = labeled
        return dictionary_with_on_off_values

    def count_on_off_values_per_time_period(self,dictionary_with_on_off_values):
        hour_dictionary ={}
        for appliance_type, pairs in dictionary_with_on_off_values.items():
            hours_count= {hour: 0 for hour in range(TOTAL_HOURS)}
            
            for timestamp, state in pairs:
                hour = pd.to_datetime(timestamp).hour
                
                if (hour in NIGHT_HOURS and state == 0) or (hour not in NIGHT_HOURS and state == 1):
                    hours_count[hour] += 1
            hour_dictionary[appliance_type] = {hour: count for hour, count in hours_count.items() if count > 0}
        return hour_dictionary