from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.base_plotter_interface import BasePlotterInterface

class SolarRadiationPLotter(BasePlotterInterface):
    def __init__(self):
        super().__init__()

    def get_data_dict(self, solar_house):
        return solar_house.solar_radiation

    def get_object_id(self, solar_house):
        return solar_house.house_id

    def get_plot_title_prefix(self):
        return "Solar Radiation House ID"

    def plot_solar_radiation_over_time(self, solar_house, month=None, day=None):
        return self.plot_over_time(solar_house, month, day)
        
    def plot_solar_radiation_over_time_range(self, solar_house, time_stamp_1, time_stamp_2):
        return self.plot_over_time_range(solar_house, time_stamp_1, time_stamp_2)
