from typing import Optional
from HouseWithAppliancesModel.house_with_appliances_builder import HouseWithAppliancesBuilder
from HouseWithAppliancesModel.house_with_appliances_preprocessing_all_houses import HouseWithAppliancesPreprocessingAllHouses
from HouseWithAppliancesModel.house_with_appliances_resampling import HouseWithAppliancesResampling
from HouseWithAppliancesModel.house_with_appliances_plotter import HouseWithAppliancesPlotter
from HouseWithAppliancesModel.house_with_appliances_statistics import HouseWithAppliancesStatistics
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption
from HouseModel.house import House

class HouseWithAppliancesFacade:
    def __init__(self) -> None:
        self.builder: HouseWithAppliancesBuilder = HouseWithAppliancesBuilder()
        self.preprocessing_data: HouseWithAppliancesPreprocessingAllHouses = HouseWithAppliancesPreprocessingAllHouses()
        self.resampling_data: HouseWithAppliancesResampling = HouseWithAppliancesResampling()
        self.plotter: HouseWithAppliancesPlotter = HouseWithAppliancesPlotter()
        self.statistics: HouseWithAppliancesStatistics = HouseWithAppliancesStatistics()

    def build_houses_with_appliances(self, csv_path: str) -> list[HouseWithAppliancesConsumption]:
        return self.builder.build(csv_path)

    def process_appliances_pipeline(self, csv_path: str, houses: list[House], export_path: Optional[str] = None) -> list[HouseWithAppliancesConsumption]:
        houses_with_appliances = self.build_houses_with_appliances(csv_path)

        houses_with_appliances = self.resampling_data.resampling_appliance_data(houses_with_appliances)

        self.preprocessing_data.matching_timestamps_between_appliance_and_house(houses_with_appliances, houses)
        self.preprocessing_data.remove_appliances_with_zero_data(houses_with_appliances)
        self.preprocessing_data.eliminate_anomalies_in_appliances(houses_with_appliances)
        self.preprocessing_data.eliminate_appliances_with_five_days_of_no_consumption(houses_with_appliances)

        if export_path:
            self.builder.export_to_csv(houses_with_appliances, export_path)

        return houses_with_appliances

    def plot_appliances_consumption_over_time(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        self.plotter.plot_all_appliances_consumption_over_time(house_with_appliances)
