import pandas as pd
import plotly.express as px
class HousePlotter:
    def __init__(self):
        pass

    def filter_values_by_month_and_day(self,house,mode, value):
        timestamps=[]
        consumptions=[]

        for key,consumption in house.consumption.items():
            timestamp=pd.to_datetime(key)
            if(mode=='month' and timestamp.month==value) or (mode=='day' and timestamp.day==value):
                timestamps.append(timestamp)
                consumptions.append(consumption)
        return timestamps, consumptions

    def plot_consumption_over_time(self,house,month=None,day=None):
        if month is None and day is None:
            fig = px.line(x=pd.to_datetime(list(house.consumption.keys())), y=list(house.consumption.values()), title=f'House ID: {house.house_id}')
            fig.show()
        if month is not None and day is None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day(house,'month', month)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {house.house_id}')
            fig.show()
        if month is None and day is not None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day(house,'day', day)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {house.house_id}')
            fig.show()
    
    def plot_consumption_over_time_range(self,house,time_stamp_1, time_stamp_2):
        time_stamp_1=pd.to_datetime(time_stamp_1)
        time_stamp_2=pd.to_datetime(time_stamp_2)
        timestamps_period=[t for t in pd.to_datetime(list(house.consumption.keys())) if time_stamp_1<=t<=time_stamp_2]
        consumption_period=[house.consumption[t] for t in timestamps_period]
        fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {house.house_id}')
        fig.show()