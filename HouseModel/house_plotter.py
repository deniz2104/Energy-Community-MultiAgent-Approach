from typing import Optional
from HelperFiles.base_plotter_interface import BasePlotterInterface
from .house import House

class HousePlotter(BasePlotterInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_data_dict(self, house: House) -> dict[str, float]:
        return house.consumption

    def get_object_id(self, house: House) -> str:
        return house.house_id

    def get_plot_title_prefix(self) -> str:
        return "House ID"

    def plot_consumption_over_time(self, house: House, month: Optional[int] = None, day: Optional[int] = None) -> None:
        return self.plot_over_time(house, month, day)
    
    def plot_consumption_over_time_range(self, house: House, time_stamp_1: str, time_stamp_2: str) -> None:
        return self.plot_over_time_range(house, time_stamp_1, time_stamp_2)