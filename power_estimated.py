from solar_radiation_house import SolarRadiationHouse
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.power_estimated = {}
    
    def add_power_estimated(self,timestamp,value,Pmax=575 , GTSTC=1000, number_of_panels=1, f=0.8):
        self.power_estimated[timestamp] = Pmax * f *number_of_panels * (value / GTSTC)
    
    def plot_power_over_time_for_a_number_of_panels(self,month=None, day=None):
        self.solar_radiation = self.power_estimated
        super().plot_consumption_over_time(month, day)

    def plot_power_over_time_range_for_a_number_of_panels(self,time_stamp_1, time_stamp_2):
        self.solar_radiation = self.power_estimated
        super().plot_consumption_over_time_range(time_stamp_1, time_stamp_2)

    def plot_power_estimated_with_consumption_over_time(self, consumption_house):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
        go.Scatter(x=(list(self.power_estimated.keys())), 
              y=list(self.power_estimated.values()),
              mode='lines', name='Power Estimated'),
        secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=(list(consumption_house.consumption.keys())), 
                    y=list(consumption_house.consumption.values()),
                    mode='lines', name='Consumption'),
            secondary_y=True,
        )

        fig.update_layout(
            title_text="Power Estimated vs. Consumption"
        )

        fig.update_yaxes(title_text="Power Estimated", secondary_y=False)
        fig.update_yaxes(title_text="Consumption", secondary_y=True)

        fig.show()