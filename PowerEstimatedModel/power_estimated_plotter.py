import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px

class PowerEstimatedPlotter:
    def __init__(self):
        pass

    def filter_values_by_month_and_day(self,power_house, mode, value):
        timestamps=[]
        consumptions=[]

        for key,consumption in power_house.power_estimated.items():
            timestamp=pd.to_datetime(key)
            if(mode=='month' and timestamp.month==value) or (mode=='day' and timestamp.day==value):
                timestamps.append(timestamp)
                consumptions.append(consumption)
        return timestamps, consumptions
    
    def plot_power_over_time_for_a_number_of_panels(self,power_house,month=None, day=None):
        if month is None and day is None:
            fig = px.line(x=pd.to_datetime(list(power_house.power_estimated.keys())), y=list(power_house.power_estimated.values()), title=f'House ID: {power_house.house_id}')
            fig.show()
        if month is not None and day is None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day(power_house,'month', month)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {power_house.house_id}')
            fig.show()
        if month is None and day is not None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day(power_house,'day', day)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {power_house.house_id}')
            fig.show()

    def plot_power_over_time_range_for_a_number_of_panels(self,power_house,time_stamp_1, time_stamp_2):
        time_stamp_1=pd.to_datetime(time_stamp_1)
        time_stamp_2=pd.to_datetime(time_stamp_2)
        timestamps_period=[t for t in pd.to_datetime(list(power_house.power_estimated.keys())) if time_stamp_1<=t<=time_stamp_2]
        power_estimated_period=[power_house.power_estimated[t] for t in timestamps_period]
        fig = px.line(x=timestamps_period, y=power_estimated_period, title=f'House ID: {power_house.house_id}')
        fig.show()

    def plot_power_estimated_with_consumption_over_time(self,power_house,consumption_house,self_consumption=None, self_sufficiency=None):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
        go.Scatter(x=(list(power_house.power_estimated.keys())), 
              y=list(power_house.power_estimated.values()),
              mode='lines', name='Power Estimated'),
        secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=(list(consumption_house.consumption.keys())), 
                    y=list(consumption_house.consumption.values()),
                    mode='lines', name='Consumption'),
            secondary_y=True,
        )

        annotations = []
        if self_consumption is not None:
            annotations.append(
                dict(
                    x=0.02,
                    y=0.98,
                    xref="paper",
                    yref="paper",
                    text=f"Self Consumption: {self_consumption.self_consumption}%",
                    showarrow=False,
                    font=dict(size=14),
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )
            )
        
        if self_sufficiency is not None:
            annotations.append(
                dict(
                    x=0.02,
                    y=0.92,
                    xref="paper",
                    yref="paper",
                    text=f"Self Sufficiency: {self_sufficiency.self_sufficiency}%",
                    showarrow=False,
                    font=dict(size=14),
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )
            )
        
        fig.update_layout(
        title_text="Power Estimated vs. Consumption",
        annotations=annotations
        )

        fig.update_yaxes(title_text="Power Estimated", secondary_y=False)
        fig.update_yaxes(title_text="Consumption", secondary_y=True)

        fig.show()