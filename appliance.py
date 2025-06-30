import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from house import House
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest 

class Appliance(House):
    def __init__(self,house_id):
        super().__init__(house_id)
        self.consumption = {}

    def add_appliance_consumption(self, timestamp, appliance_type, value):
        self.consumption.setdefault(appliance_type, []).append((timestamp, value))

    def eliminate_days_after_a_year(self,house):
        starting_time,ending_time = house.show_starting_time_and_ending_time()
        new_dictionary={}

        starting_time = pd.to_datetime(starting_time)
        ending_time = pd.to_datetime(ending_time)

        for appliance_type,pairs in self.consumption.items():
            new_pairs=[]
            timestamps=[pair[0] for pair in pairs]
            datatime_timestamps=pd.to_datetime(timestamps)
            for i,(timestamp,value) in enumerate(pairs):
                if starting_time <= datatime_timestamps[i] <= ending_time:
                    new_pairs.append((timestamp, value))
            new_dictionary[appliance_type]=new_pairs
        self.consumption=new_dictionary
        new_dictionary=None
    
    def plot_all_appliances_consumption_over_time(self):
        fig = make_subplots(rows=len(self.consumption), cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(self.consumption.items()):
            timestamps = [pair[0] for pair in consumption]
            values = [pair[1] for pair in consumption]
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i+1, col=1)

        fig.update_layout(title_text="Appliances Consumption Over Time", showlegend=False)
        fig.show()


    def count_zeros_in_consumption(self):
        return {appliance_type: sum(value == 0 for _, value in consumption) for appliance_type, consumption in self.consumption.items()}
    
    def eliminate_appliances_with_lot_of_zeros_consumption(self):
        appliances_with_enough_data = {appliance_type: consumption for appliance_type, consumption in self.consumption.items() if sum(value == 0 for _, value in consumption) < len(consumption)-len(consumption)//24}
        self.consumption = appliances_with_enough_data
    
    def eliminate_anomalies_in_my_data(self):
        new_consumption = {}
        
        for appliance_type, pairs in self.consumption.items():
            timestamps = [pair[0] for pair in pairs]
            values = [pair[1] for pair in pairs]
            
            temp_consumption = dict(zip(timestamps, values))
            
            temp_house = House(self.house_id)
            temp_house.consumption = temp_consumption
            temp_house.eliminate_anomalies_in_data()
            
            filtered_pairs = [(timestamp, value) for timestamp, value in temp_house.consumption.items()]
            
            if filtered_pairs:
                new_consumption[appliance_type] = filtered_pairs
        
        self.consumption = new_consumption

    def eliminate_appliance_with_five_days_of_no_consumption(self):
        new_consumption = {}

        for appliance_type, pairs in self.consumption.items():
            timestamps = [pair[0] for pair in pairs]
            values = [pair[1] for pair in pairs]
            
            temp_consumption = dict(zip(timestamps, values))
            
            temp_house = House(self.house_id)
            temp_house.consumption = temp_consumption
            
            if (temp_house.remove_houses_having_zero_for_a_period_of_time(is_appliance=True)==0):
                filtered_pairs = [(timestamp, value) for timestamp, value in temp_house.consumption.items()]
                new_consumption[appliance_type] = filtered_pairs        
        self.consumption = new_consumption

    def kmeans_clustering(self,data_for_kmeans, number_of_clusters=2):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_for_kmeans)
        kmeans = KMeans(n_clusters=number_of_clusters, random_state=42, n_init=50)
        kmeans.fit_predict(scaled_data)
        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        return scaler,kmeans,centroids
            
    def return_chunk_values(self,chunk,kmeans,scaler,on_cluster_label=None,off_cluster_label=None):
        if on_cluster_label is None:
            data_chunks = [
                    chunk[j]
                    for j in range(len(chunk))
                    if kmeans.predict(scaler.transform([[chunk[j][1]]]))[0] == off_cluster_label
                ]
        else:
            data_chunks = [
                    chunk[j]
                    for j in range(len(chunk))
                    if kmeans.predict(scaler.transform([[chunk[j][1]]]))[0] == on_cluster_label
                ]
        return data_chunks            
    def determine_on_off_periods(self,chunk_size=168):
        dictionary_with_off_values = {}
        for appliance_type, pairs in self.consumption.items():
            dictionary_with_off_values.setdefault(appliance_type, [])
            off_pairs = []
            on_pairs = []
            for i in range(0,len(pairs),chunk_size):
                chunk= pairs[i:i+chunk_size]
                chunk = list(set(chunk))
                data_for_kmeans = np.array([pair[1] for pair in chunk]).reshape(-1, 1)
                scaler,kmeans,centroids = self.kmeans_clustering(data_for_kmeans)
                off_cluster_label = np.argmin(centroids)
                on_cluster_label = np.argmax(centroids)
                chunk_on = self.return_chunk_values(chunk,kmeans,scaler,on_cluster_label)
                on_pairs.extend(chunk_on)
                chunk_off = self.return_chunk_values(chunk,kmeans,scaler,None,off_cluster_label)
                off_pairs.extend(chunk_off)
                off_pairs_labeled = [(timestamp, 0) for timestamp, _ in off_pairs]
                on_pairs_labeled = [(timestamp, 1) for timestamp, _ in on_pairs]
            dictionary_with_off_values[appliance_type] = off_pairs_labeled + on_pairs_labeled
        return dictionary_with_off_values
    
    def plot_points_of_interest(self,dictionary_with_on_off_values):
        fig = make_subplots(rows=len(self.consumption)*2, cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(self.consumption.items()):
            timestamps = [pair[0] for pair in consumption]
            values = [pair[1] for pair in consumption]
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i*2+1, col=1)
        
        for i, (appliance_type, points_of_interest) in enumerate(dictionary_with_on_off_values.items()):
            timestamps = [pair[0] for pair in points_of_interest]
            values = [pair[1] for pair in points_of_interest]
            fig.add_trace(go.Scatter(x=timestamps, y=values, mode='markers', name=f"{appliance_type} On and Off values", marker=dict(color='red')), row=i*2+2, col=1)
    
        fig.show()