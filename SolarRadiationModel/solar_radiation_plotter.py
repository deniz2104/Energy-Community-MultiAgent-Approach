from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.base_plotter_interface import BasePlotterInterface
from .solar_radiation_house import SolarRadiationHouse

class SolarRadiationPlotter(BasePlotterInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_data_dict(self, solar_house: SolarRadiationHouse) -> dict[str, float]:
        return solar_house.solar_radiation

    def get_object_id(self, solar_house: SolarRadiationHouse) -> int:
        return solar_house.house_id

    def get_plot_title_prefix(self) -> str:
        return "Solar Radiation House ID"

    def plot_solar_radiation_over_time(self, solar_house: SolarRadiationHouse, month: int = None, day: int = None) -> None:
        return self.plot_over_time(solar_house, month, day)

    def plot_solar_radiation_over_time_range(self, solar_house: SolarRadiationHouse, time_stamp_1: str, time_stamp_2: str) -> None:
        return self.plot_over_time_range(solar_house, time_stamp_1, time_stamp_2)
