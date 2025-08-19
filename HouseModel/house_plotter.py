from typing import Optional
from HelperFiles.base_plotter_interface import BasePlotterInterface
from HouseModel.house import House

class HousePlotter(BasePlotterInterface):
    def get_data_dict(self, data_object: House) -> dict[str, float]:
        return data_object.consumption

    def get_object_id(self, data_object: House) -> int:
        return data_object.house_id

    def get_plot_title_prefix(self) -> str:
        return "House ID"

    def plot_consumption_over_time(self, house: House, month: Optional[int] = None, day: Optional[int] = None) -> None:
        return self.plot_over_time(house, month, day)
    
    def plot_consumption_over_time_range(self, house: House, time_stamp_1: str, time_stamp_2: str) -> None:
        return self.plot_over_time_range(house, time_stamp_1, time_stamp_2)