from typing import Optional
from .house_with_appliances_builder import HouseWithAppliancesBuilder
from .house_with_appliances_preprocessing_data import HouseWithAppliancesPreprocessingData
from .house_with_appliances_resampling import HouseWithAppliancesResampling
from .house_with_appliances_plotter import HouseWithAppliancesPlotter
from .house_with_appliances_statistics import HouseWithAppliancesStatistics
from .house_with_appliances_label_for_on_and_off_values import HouseWithAppliancesOnOffValues
from .determine_which_appliance_consumes_more import DetermineWhichApplianceConsumesMore
from .house_with_appliances import HouseWithAppliancesConsumption
from HouseModel.house import House
from HelperFiles.file_to_handle_absolute_path_imports import *

class HouseWithAppliancesFacade:
    def __init__(self) -> None:
        self.builder: HouseWithAppliancesBuilder = HouseWithAppliancesBuilder()
        self.preprocessor: HouseWithAppliancesPreprocessingData = HouseWithAppliancesPreprocessingData()
        self.resampler: HouseWithAppliancesResampling = HouseWithAppliancesResampling()
        self.plotter: HouseWithAppliancesPlotter = HouseWithAppliancesPlotter()
        self.data_labeler: HouseWithAppliancesOnOffValues = HouseWithAppliancesOnOffValues()
        self.statistics: HouseWithAppliancesStatistics = HouseWithAppliancesStatistics()
        self.determine_which_appliance_consumes_more: DetermineWhichApplianceConsumesMore = DetermineWhichApplianceConsumesMore()

    def build_houses_with_appliances(self, csv_path: str) -> list[HouseWithAppliancesConsumption]:
        return self.builder.build(csv_path)

    def process_appliances_pipeline(self, csv_path: str, houses: list[House], export_path: Optional[str] = None) -> list[HouseWithAppliancesConsumption]:
        houses_with_appliances = self.build_houses_with_appliances(csv_path)

        houses_with_appliances = self.resampler.resampling_appliance_data(houses_with_appliances)

        self.preprocessor.matching_timestamps_between_appliance_and_house(houses_with_appliances, houses)

        self.preprocessor.remove_appliances_with_zero_data(houses_with_appliances)

        self.preprocessor.eliminate_anomalies_in_appliances(houses_with_appliances)

        self.preprocessor.eliminate_appliances_with_five_days_of_no_consumption(houses_with_appliances)

        if export_path:
            self.builder.export_to_csv(houses_with_appliances, export_path)

        return houses_with_appliances

    def see_on_off_patterns(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, list[tuple[str, int]]]:
        return self.data_labeler.determine_on_off_periods(house_with_appliances)

    def show_hours_distribution(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[int, int]]:
        on_off_dict = self.data_labeler.determine_on_off_periods(house_with_appliances)
        return self.data_labeler.count_on_off_values_per_time_period(on_off_dict)

    def plot_appliances_and_on_off_values(self, house_with_appliances: HouseWithAppliancesConsumption, on_off_dict: Optional[dict[str, list[tuple[str, int]]]] = None, plot_on_off: bool = True) -> None:
        self.plotter.plot_all_appliances_consumption_over_time(house_with_appliances)
        if plot_on_off and on_off_dict is not None:
            self.plotter.plot_appliances_and_on_off_values(house_with_appliances, on_off_dict)

    def show_hours_weights(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[int, float]]:
        hours_distribution = self.show_hours_distribution(house_with_appliances)
        return self.statistics.determine_hours_weights(hours_distribution)

    def show_appliance_histogram(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        hours_distribution = self.show_hours_distribution(house_with_appliances)
        for appliance_name, hours in hours_distribution.items():
            self.plotter.plot_appliance_histogram(hours, appliance_name)

    def show_appliance_mean_consumption_based_on_hour(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[int, float]]:
        on_off_dict = self.see_on_off_patterns(house_with_appliances)
        hours_distribution = self.show_hours_distribution(house_with_appliances)
        return self.statistics.get_mean_consumption_by_hour(house_with_appliances, on_off_dict, hours_distribution)

    def show_consumption_along_with_sigmoid_values(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        self.determine_which_appliance_consumes_more.show_sigmoid_values_along_with_consumption_values(house_with_appliances)

    def show_histogram(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        self.determine_which_appliance_consumes_more.plot_sigmoid_distribution_bins(house_with_appliances)