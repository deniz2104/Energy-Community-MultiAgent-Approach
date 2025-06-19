import pandas as pd
from house import House
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        
