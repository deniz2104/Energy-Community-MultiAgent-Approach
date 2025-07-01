from solar_radiation_house import SolarRadiationHouse
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.power_estimated = {}
        self.NEEG_on_period= {}
        self.NEEG= None
    
    def add_power_estimated(self,timestamp,value,Pmax=575 , GTSTC=1000, number_of_panels=1, f=0.8):
        self.power_estimated[timestamp] = Pmax * f *number_of_panels * (value / GTSTC)

    def determine_NEEG(self):
        self.NEEG = sum(
            min(self.power_estimated.get(ts, 0), self.consumption.get(ts, 0))
            for ts in self.power_estimated
        ) 
    
    def plot_power_over_time_for_a_number_of_panels(self,month=None, day=None):
        self.solar_radiation = self.power_estimated
        super().plot_consumption_over_time(month, day)

    def plot_power_over_time_range_for_a_number_of_panels(self,time_stamp_1, time_stamp_2):
        self.solar_radiation = self.power_estimated
        super().plot_consumption_over_time_range(time_stamp_1, time_stamp_2)

    def plot_power_estimated_with_consumption_over_time(self, consumption_house,self_consumption=None, self_sufficiency=None):
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