from typing import Optional
from .power_estimated_builder import PowerEstimatedBuilder
from .power_estimated_plotter import PowerEstimatedPlotter
from .power_estimated import PowerEstimator
from HouseModel.house import House

class PowerEstimatedFacade:
    def __init__(self) -> None:
        self.builder: PowerEstimatedBuilder = PowerEstimatedBuilder()
        self.plotter: PowerEstimatedPlotter = PowerEstimatedPlotter()

    def build_power_estimated_data(self, csv_path: str) -> list[PowerEstimator]:
        return self.builder.build(csv_path)
    
    def determine_NEEG_for_all_houses(self, power_estimated: list[PowerEstimator]) -> None:
        self.builder.determine_NEEG_for_all_houses(power_estimated)

    def plot_power_estimated_data(self, power_estimated: PowerEstimator) -> None:
        self.plotter.plot_power_over_time_for_a_number_of_panels(power_estimated)

    def plot_power_estimated_data_with_consumption(self, power_estimated: PowerEstimator, consumption_house: House, self_consumption: Optional[float] = None, self_sufficiency: Optional[float] = None) -> None:
        self.plotter.plot_power_estimated_with_consumption_over_time(power_estimated, consumption_house, self_consumption, self_sufficiency)