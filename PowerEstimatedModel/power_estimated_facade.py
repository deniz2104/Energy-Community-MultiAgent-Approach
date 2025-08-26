from typing import Optional
from PowerEstimatedModel.power_estimated_builder import PowerEstimatedBuilder
from PowerEstimatedModel.power_estimated_plotter import PowerEstimatedPlotter
from PowerEstimatedModel.power_estimated import PowerEstimator
from PowerEstimatedModel.power_estimated_attribute_adder import PowerEstimatedAttributeAdder
from HouseModel.house import House

class PowerEstimatedFacade:
    def __init__(self) -> None:
        self.builder= PowerEstimatedBuilder()
        self.plotter= PowerEstimatedPlotter()
        self.add_attribute_to_agent = PowerEstimatedAttributeAdder()

    def build_power_estimated_data(self, csv_path: str) -> list[PowerEstimator]:
        return self.builder.build(csv_path)

    def determine_NEEG_for_all_houses(self, houses_with_power_estimated: list[PowerEstimator]) -> None:
        self.builder.determine_NEEG_for_all_houses(houses_with_power_estimated)

    def plot_power_estimated_data(self, house_with_power_estimated: PowerEstimator) -> None:
        self.plotter.plot_power_over_time_for_a_number_of_panels(house_with_power_estimated)

    def plot_power_estimated_data_with_consumption(self, house_with_power_estimated: PowerEstimator, consumption_house: House, self_consumption: Optional[float] = None, self_sufficiency: Optional[float] = None) -> None:
        self.plotter.plot_power_estimated_with_consumption_over_time(house_with_power_estimated, consumption_house, self_consumption, self_sufficiency)

    def add_power_estimated_attribute_to_houses(self, houses: list[House], houses_with_power_estimated: list[PowerEstimator]) -> None:
        self.add_attribute_to_agent.add_power_estimated_to_houses(houses, houses_with_power_estimated)
