from .power_estimated_builder import PowerEstimatedBuilder
from .power_estimated_plotter import PowerEstimatedPlotter

class PowerEstimatedFacade:
    def __init__(self):
        self.builder = PowerEstimatedBuilder()
        self.plotter = PowerEstimatedPlotter()

    def build_power_estimated_data(self, csv_path):
        return self.builder.build(csv_path)
    
    def determine_NEEG_for_all_houses(self, power_estimated):
        self.builder.determine_NEEG_for_all_houses(power_estimated)

    def plot_power_estimated_data(self, power_estimated):
        self.plotter.plot_power_over_time_for_a_number_of_panels(power_estimated)

    def plot_power_estimated_data_with_consumption(self, power_estimated, consumption_house, self_consumption=None, self_sufficiency=None):
        self.plotter.plot_power_estimated_with_consumption_over_time(power_estimated, consumption_house, self_consumption, self_sufficiency)