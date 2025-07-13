from .house import House
from collections import OrderedDict
import pandas as pd
class HouseResampler:
    def __init__(self):
        pass

    def prepare_house_for_resampling(self,house):
        df=pd.DataFrame(list(house.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp']=pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        df.sort_index(inplace=True)

        df_hourly=df.resample('h').mean()
        timestamps=df_hourly.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        consumption=df_hourly['Consumption'].tolist()
        return timestamps, consumption

    def resampling_houses_based_on_time_period(self, houses):
        resampled_houses={}
        for house in houses:
            timestamps, consumption = self.prepare_house_for_resampling(house)
            resampled_house = House(house.house_id)
            resampled_houses[house.house_id] = resampled_house

            for ts, cons in zip(timestamps, consumption):
                resampled_house.add_consumption(ts, cons)

            sorted_consumption = sorted(resampled_house.consumption.items(), key=lambda x: x[0])
            resampled_house.consumption = OrderedDict(sorted_consumption)
        return list(resampled_houses.values())