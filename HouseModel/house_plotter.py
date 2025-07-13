from HelperFiles.base_plotter_interface import BasePlotterInterface

class HousePlotter(BasePlotterInterface):
    def __init__(self):
        super().__init__()

    def get_data_dict(self, house):
        return house.consumption

    def get_object_id(self, house):
        return house.house_id

    def get_plot_title_prefix(self):
        return "House ID"

    def plot_consumption_over_time(self, house, month=None, day=None):
        return self.plot_over_time(house, month, day)
    
    def plot_consumption_over_time_range(self, house, time_stamp_1, time_stamp_2):
        return self.plot_over_time_range(house, time_stamp_1, time_stamp_2)