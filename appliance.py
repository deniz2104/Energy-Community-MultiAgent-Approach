import pandas as pd
from house import House
from collections import OrderedDict

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
