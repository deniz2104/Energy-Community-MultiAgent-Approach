from house import House
import pandas as pd
import plotly.express as px

class SolarRadiationHouse(House):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.solar_radiation = {}
    def add_solar_radiation(self, timestamp, value):
        self.solar_radiation[timestamp] = value
    def plot_consumption_over_time(self, month=None, day=None):
        temp_consumption = self.consumption
        
        self.consumption = self.solar_radiation
        
        super().plot_consumption_over_time(month, day)
        
        self.consumption = temp_consumption
    def plot_consumption_over_time_range(self, time_stamp_1, time_stamp_2):
        temp_consumption = self.consumption
        self.consumption = self.solar_radiation
        super().plot_consumption_over_time_range(time_stamp_1, time_stamp_2)
        self.consumption = temp_consumption
    def plot_radiation_with_consumption_over_time(self, month=None, day=None):
        fig = px.scatter(x=pd.to_datetime(list(self.solar_radiation.keys())), y=list(self.solar_radiation.values()), title=f'House ID: {self.house_id}, Solar Radiation')
        fig.add_trace(px.scatter(x=pd.to_datetime(list(self.solar_radiation.keys())), y=self.consumption, title=f'House ID: {self.house_id}, Consumption'))
        fig.show()

    def change_timing_for_solar_radiation(self, house):
        if house.house_id != self.house_id:
            print(f'House {self.house_id} does not exist in the consumption data.')
            return
    
        starting_time, ending_time = house.show_starting_time_and_ending_time()
        if starting_time and ending_time:
            print(f'Changing solar radiation timing for house {self.house_id} from {starting_time} to {ending_time}')
        
            starting_time = pd.to_datetime(starting_time)
            ending_time = pd.to_datetime(ending_time)
        
            self.solar_radiation = {
                t: v for t, v in self.solar_radiation.items()
                if starting_time <= pd.to_datetime(t) <= ending_time
        }
        
        print(f'Filtered solar radiation data: {len(self.solar_radiation)} points')