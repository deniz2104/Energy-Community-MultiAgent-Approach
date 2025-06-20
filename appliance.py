import pandas as pd
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
        for appliance_type, pairs in self.consumption.items():
            df=pd.DataFrame(pairs, columns=['Timestamp', 'Consumption'])
            df['Timestamp']=pd.to_datetime(df['Timestamp'])
            isolation_forest = IsolationForest(n_estimators=300,contamination=0.0002,random_state=42)
            isolation_forest.fit(df[['Consumption']])
            df['anomaly'] = isolation_forest.predict(df[['Consumption']])

            anomalies_df = df[df['anomaly'] == -1]
            anomalous_values = anomalies_df['Consumption'].values.tolist()
        
            filtered_pairs = [(timestamp, value) for timestamp, value in pairs if value not in anomalous_values]
            self.consumption[appliance_type]=filtered_pairs

