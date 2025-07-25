from abc import ABC, abstractmethod
from typing import Any,Optional
import pandas as pd
import plotly.express as px

class BasePlotterInterface(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def get_data_dict(self, data_object: Any) -> dict[str, float]:
        pass
    
    @abstractmethod
    def get_object_id(self, data_object: Any) -> int:
        pass
    
    @abstractmethod
    def get_plot_title_prefix(self) -> str:
        pass

    def filter_values_by_month_and_day(self, data_object: Any, mode: str, value: int) -> tuple[list[pd.Timestamp], list[float]]:
        timestamps = []
        values = []
        
        data_dict = self.get_data_dict(data_object)
        for key, data_value in data_dict.items():
            timestamp = pd.to_datetime(key)
            if (mode == 'month' and timestamp.month == value) or (mode == 'day' and timestamp.day == value):
                timestamps.append(timestamp)
                values.append(data_value)
        return timestamps, values
    
    def plot_over_time(self, data_object: Any, month: Optional[int] = None, day: Optional[int] = None) -> None:
        object_id = self.get_object_id(data_object)
        title_prefix = self.get_plot_title_prefix()
        
        if month is None and day is None:
            data_dict = self.get_data_dict(data_object)
            fig = px.line(
                x=pd.to_datetime(list(data_dict.keys())), 
                y=list(data_dict.values()), 
                title=f'{title_prefix}: {object_id}'
            )
            fig.show()
        elif month is not None and day is None:
            timestamps_period, values_period = self.filter_values_by_month_and_day(data_object, 'month', month)
            fig = px.line(
                x=timestamps_period, 
                y=values_period, 
                title=f'{title_prefix}: {object_id} - Month {month}'
            )
            fig.show()
        elif month is None and day is not None:
            timestamps_period, values_period = self.filter_values_by_month_and_day(data_object, 'day', day)
            fig = px.line(
                x=timestamps_period, 
                y=values_period, 
                title=f'{title_prefix}: {object_id} - Day {day}'
            )
            fig.show()
    
    def plot_over_time_range(self, data_object: Any, time_stamp_1: str, time_stamp_2: str) -> None:
        time_stamp_1 = pd.to_datetime(time_stamp_1)
        time_stamp_2 = pd.to_datetime(time_stamp_2)
        
        data_dict = self.get_data_dict(data_object)
        timestamps_period = [t for t in pd.to_datetime(list(data_dict.keys())) if time_stamp_1 <= t <= time_stamp_2]
        values_period = [data_dict[str(t)] for t in timestamps_period]
        
        object_id = self.get_object_id(data_object)
        title_prefix = self.get_plot_title_prefix()
        
        fig = px.line(
            x=timestamps_period, 
            y=values_period, 
            title=f'{title_prefix}: {object_id} - {time_stamp_1.date()} to {time_stamp_2.date()}'
        )
        fig.show()
