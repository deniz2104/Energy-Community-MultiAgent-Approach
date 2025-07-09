import pandas as pd
import plotly.express as px
from HelperFiles.file_to_handle_absolute_path_imports import *
class SolarRadiationPLotter():
    def __init__(self):
        pass

    def filter_values_by_month_and_day(self,solar_house, mode, value):
        timestamps=[]
        consumptions=[]

        for key,consumption in solar_house.solar_radiation.items():
            timestamp=pd.to_datetime(key)
            if(mode=='month' and timestamp.month==value) or (mode=='day' and timestamp.day==value):
                timestamps.append(timestamp)
                consumptions.append(consumption)
        return timestamps, consumptions
    def plot_solar_radiation_over_time(self,solar_house, month=None, day=None):        
        if month is None and day is None:
            fig = px.line(x=pd.to_datetime(list(solar_house.solar_radiation.keys())), y=list(solar_house.solar_radiation.values()), title=f'House ID: {solar_house.house_id}')
            fig.show()
        if month is not None and day is None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day(solar_house,'month', month)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {solar_house.house_id}')
            fig.show()
        if month is None and day is not None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day(solar_house,'day', day)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {solar_house.house_id}')
            fig.show()
        
    def plot_solar_radiation_over_time_range(self,solar_house, time_stamp_1, time_stamp_2):
        time_stamp_1=pd.to_datetime(time_stamp_1)
        time_stamp_2=pd.to_datetime(time_stamp_2)
        timestamps_period=[t for t in pd.to_datetime(list(solar_house.solar_radiation.keys())) if time_stamp_1<=t<=time_stamp_2]
        solar_radiation_period=[solar_house.solar_radiation[t] for t in timestamps_period]
        fig = px.line(x=timestamps_period, y=solar_radiation_period, title=f'House ID: {solar_house.house_id}')
        fig.show()
