from PowerEstimatedModel.power_estimated import PowerEstimator
from typing import Optional
from HouseModel.house import House
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from HelperFiles.base_plotter_interface import BasePlotterInterface
from HelperFiles.file_to_handle_absolute_path_imports import *

class PowerEstimatedPlotter(BasePlotterInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_data_dict(self, power_house: PowerEstimator) -> dict[str, float]:
        return power_house.power_estimated

    def get_object_id(self, power_house: PowerEstimator) -> int:
        return power_house.house_id

    def get_plot_title_prefix(self) -> str:
        return "Power Estimated House ID"

    def plot_power_over_time_for_a_number_of_panels(self, power_house: PowerEstimator, month: Optional[int] = None, day: Optional[int] = None) -> None:
        return self.plot_over_time(power_house, month, day)

    def _plot_power_over_time_range_for_a_number_of_panels(self, power_house: PowerEstimator, time_stamp_1: str, time_stamp_2: str) -> None:
        return self.plot_over_time_range(power_house, time_stamp_1, time_stamp_2)

    def _make_annotations(self, self_consumption: Optional[float] = None, self_sufficiency: Optional[float] = None) -> list[dict]:
        annotations = []
        if self_consumption is not None:
            annotations.append(
                dict(x=0.02,y=0.98,
                    xref="paper",yref="paper",
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
                    x=0.02,y=0.92,
                    xref="paper",yref="paper",
                    text=f"Self Sufficiency: {self_sufficiency.self_sufficiency}%",
                    showarrow=False,
                    font=dict(size=14),
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )
            )
        return annotations

    def _update_layout(self, fig: go.Figure, annotations: list[dict]) -> go.Figure:
        fig.update_layout(title_text="Power Estimated vs. Consumption",
        annotations=annotations
        )

        fig.update_yaxes(title_text="Power Estimated", secondary_y=False)
        fig.update_yaxes(title_text="Consumption", secondary_y=True)
        return fig


    def plot_power_estimated_with_consumption_over_time(self,power_house : PowerEstimator ,consumption_house: House ,self_consumption: Optional[float] =None, self_sufficiency : Optional[float] =None) -> None:
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

        annotations = self._make_annotations(self_consumption, self_sufficiency)
        
        fig = self._update_layout(fig, annotations)

        fig.show()