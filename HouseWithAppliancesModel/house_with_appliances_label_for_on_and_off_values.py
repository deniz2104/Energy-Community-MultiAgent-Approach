from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from .house_with_appliances import HouseWithAppliancesConsumption
from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import NIGHT_HOURS,TOTAL_HOURS

class HouseWithAppliancesOnOffValues:
    def __init__(self):
        self.random_state :int = 42
        self.chunk_size :int = 168
        self.number_of_clusters :int = 2

    def cluster_data(self,data_for_kmeans : np.ndarray) -> tuple[StandardScaler, KMeans, np.ndarray]:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_for_kmeans)

        kmeans = KMeans(n_clusters=self.number_of_clusters, random_state=self.random_state, n_init=50)
        kmeans.fit_predict(scaled_data)

        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler,kmeans,centroids

    def filter_by_cluster(self,chunk_of_values:np.ndarray,kmeans:KMeans,scaler:StandardScaler,label:int) -> list[tuple[str, float]]:
        return [data_point for data_point in chunk_of_values if kmeans.predict(scaler.transform([[data_point[1]]]))[0] == label]

    def determine_on_off_periods(self,house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[int, int]]:
        dictionary_with_on_off_values :dict[str, dict[int, int]] = {}
        for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
            off_pairs, on_pairs = [], []
            values=list(consumption.values())

            for i in range(0, len(values), self.chunk_size):
                timestamps_chunk = list(consumption.keys())[i:i+self.chunk_size]
                values_chunk = values[i:i+self.chunk_size]
                chunk_of_values_and_timestamps = list(zip(timestamps_chunk, values_chunk))
                consumption_values = np.array(np.unique(values_chunk)).reshape(-1, 1)
                scaler, kmeans, centroids = self.cluster_data(consumption_values)

                off_label = np.argmin(centroids)
                on_label = np.argmax(centroids)

                off_pairs.extend(self.filter_by_cluster(chunk_of_values_and_timestamps, kmeans, scaler, off_label))
                on_pairs.extend(self.filter_by_cluster(chunk_of_values_and_timestamps, kmeans, scaler, on_label))
            
            labeled = {timestamp: 0 for (timestamp, _) in off_pairs} | {timestamp: 1 for (timestamp, _) in on_pairs}
            dictionary_with_on_off_values[appliance_type] = labeled
        return dictionary_with_on_off_values