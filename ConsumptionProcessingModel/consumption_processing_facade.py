import numpy as np
from typing import Optional
from ConsumptionProcessingModel.house_with_appliances_manage_data_after_labeling import HouseWithAppliancesManageDataAfterLabeling
from ConsumptionProcessingModel.house_with_appliances_label_for_on_and_off_values import HouseWithAppliancesOnOffValues
from ConsumptionProcessingModel.consumption_data_processor import ConsumptionDataProcessor
from ConsumptionProcessingModel.sigmoid_analyzer import SigmoidAnalyzer
from ConsumptionProcessingModel.consumption_clusterer import ConsumptionClusterer
from ConsumptionProcessingModel.consumption_processing_plotter import ConsumptionProcessingPlotter
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption

class ConsumptionProcessingFacade:
    """
    Facade class for consumption processing, clustering, labeling, and analysis operations.
    This class provides a unified interface for all consumption-related data processing
    including on/off pattern detection, threshold determination, and sigmoid analysis.
    """
    
    def __init__(self) -> None:
        self.data_labeler: HouseWithAppliancesOnOffValues = HouseWithAppliancesOnOffValues()
        self.manage_data_after_labeling: HouseWithAppliancesManageDataAfterLabeling = HouseWithAppliancesManageDataAfterLabeling()
        self.data_processor: ConsumptionDataProcessor = ConsumptionDataProcessor()
        self.sigmoid_analyzer: SigmoidAnalyzer = SigmoidAnalyzer()
        self.consumption_clusterer: ConsumptionClusterer = ConsumptionClusterer()
        self.plotter: ConsumptionProcessingPlotter = ConsumptionProcessingPlotter()

    def see_on_off_patterns(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[str, int]]:
        return self.data_labeler.determine_on_off_periods(house_with_appliances)

    def show_hours_distribution(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[int, int]]:
        on_off_dict = self.data_labeler.determine_on_off_periods(house_with_appliances)
        return self.manage_data_after_labeling.count_on_off_values_per_time_period(on_off_dict)

    def gather_off_values(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, np.ndarray]:
        return self.manage_data_after_labeling.gather_off_values_per_appliance(house_with_appliances)
    
    def determine_appliance_thresholds(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, float]:
        off_values = self.gather_off_values(house_with_appliances)
        return self.consumption_clusterer.determine_threshold(house_with_appliances, off_values)

    def show_sigmoid_distribution(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        off_values = self.gather_off_values(house_with_appliances)
        self.sigmoid_analyzer.plot_sigmoid_distribution_bins(house_with_appliances, off_values)

    def get_consumption_histogram_data(self, house_with_appliances: HouseWithAppliancesConsumption) -> tuple[list[str], dict]:
        off_values = self.gather_off_values(house_with_appliances)
        return self.sigmoid_analyzer.gather_labels_and_counts(house_with_appliances, off_values)

    def process_consumption_data(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, np.ndarray]:
        off_values = self.gather_off_values(house_with_appliances)
        clean_data = self.data_processor.eliminate_off_values_from_each_appliance(house_with_appliances, off_values)
        return self.data_processor.determine_sigmoid_values_for_each_appliance(clean_data)

    def get_consumption_values_for_appliances(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, np.ndarray]:
        return self.data_processor.gather_consumption_values_for_each_appliance(house_with_appliances)

    # Plotting Methods
    def plot_appliances_and_on_off_values(self, house_with_appliances: HouseWithAppliancesConsumption, on_off_dict: Optional[dict[str, dict[str, int]]] = None) -> None:
        if on_off_dict is None:
            on_off_dict = self.see_on_off_patterns(house_with_appliances)
        self.plotter.plot_appliances_and_on_off_values(house_with_appliances, on_off_dict)

    def plot_appliance_usage_histogram(self, house_with_appliances: HouseWithAppliancesConsumption, appliance_name: Optional[str] = None, is_night: bool = False) -> None:
        hours_distribution = self.show_hours_distribution(house_with_appliances)
        
        if appliance_name and appliance_name in hours_distribution:
            self.plotter.plot_appliance_histogram(hours_distribution[appliance_name], appliance_name, is_night)
        elif appliance_name is None:
            for appliance, hours in hours_distribution.items():
                self.plotter.plot_appliance_histogram(hours, appliance, is_night)