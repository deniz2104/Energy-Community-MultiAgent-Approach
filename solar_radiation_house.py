from house import House
import pandas as pd

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