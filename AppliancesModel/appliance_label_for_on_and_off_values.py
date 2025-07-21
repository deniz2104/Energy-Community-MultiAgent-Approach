from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import NIGHT_HOURS,TOTAL_HOURS

class ApplianceOnOffValues:
    def __init__(self):
        pass

    def kmeans_clustering(self,data_for_kmeans, number_of_clusters=2):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_for_kmeans)
        kmeans = KMeans(n_clusters=number_of_clusters, random_state=42, n_init=50)
        kmeans.fit_predict(scaled_data)
        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler,kmeans,centroids
            
    def return_chunk_values(self,chunk,kmeans,scaler,on_cluster_label=None,off_cluster_label=None):
        if on_cluster_label is None:
            label = off_cluster_label
        else:
            label = on_cluster_label
        data_chunks = [chunk[j]
                       for j in range(len(chunk))
                    if kmeans.predict(scaler.transform([[chunk[j][1]]]))[0] == label]
        return data_chunks            
    def determine_on_off_periods(self,appliance,chunk_size=168):
        dictionary_with_on_off_values = {}
        for appliance_type, pairs in appliance.appliance_consumption.items():
            off_pairs, on_pairs = [], []
            for i in range(0, len(pairs), chunk_size):
                chunk = list(set(pairs[i:i+chunk_size]))
                data_for_kmeans = np.array([pair[1] for pair in chunk]).reshape(-1, 1)
                scaler, kmeans, centroids = self.kmeans_clustering(data_for_kmeans)
                off_label = np.argmin(centroids)
                on_label = np.argmax(centroids)
                off_pairs.extend(self.return_chunk_values(chunk, kmeans, scaler, None, off_label))
                on_pairs.extend(self.return_chunk_values(chunk, kmeans, scaler, on_label))
            labeled = [(ts, 0) for ts, _ in off_pairs] + [(ts, 1) for ts, _ in on_pairs]
            dictionary_with_on_off_values[appliance_type] = labeled
        return dictionary_with_on_off_values

    def count_on_off_values_per_time_period(self,dictionary_with_on_off_values):
        hour_dictionary ={}
        for appliance_type, pairs in dictionary_with_on_off_values.items():
            hour_dictionary[appliance_type] = []
            hours= {hour: 0 for hour in range(TOTAL_HOURS)}
            for timestamp, value in pairs:
                hour = pd.to_datetime(timestamp).hour
                if (hour in NIGHT_HOURS) and value == 0:
                    hours[hour] += 1
                if (hour not in NIGHT_HOURS) and value == 1:
                    hours[hour] += 1
            hour_dictionary[appliance_type] = hours
            hour_dictionary[appliance_type] = {hour: count for hour, count in hours.items() if count > 0}
        return hour_dictionary

    def determine_off_dictionary_for_night(self,appliance,dictionary_with_on_off_values):
        off_values_list=[]
        for appliance_type,pairs in dictionary_with_on_off_values.items():
            for timestamp,value in pairs:
                hour=pd.to_datetime(timestamp).hour
                if(hour in NIGHT_HOURS) and value == 0:
                    off_values_list.append(appliance.dict(appliance_consumption[appliance_type]).get(timestamp))
        return np.unique(np.trim_zeros(np.array(off_values_list)))
