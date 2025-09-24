import numpy as np
import plotly.graph_objects as go
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption
from ConsumptionProcessingModel.consumption_data_processor import ConsumptionDataProcessor

class SigmoidAnalyzer:
    def __init__(self) -> None:
        self.data_percentile = 75.0
        self._data_processor = ConsumptionDataProcessor()

    def gather_labels_and_counts(self, house_with_appliances: HouseWithAppliancesConsumption, off_values: dict[str, np.ndarray]) -> tuple[list[str], dict]:
        all_consumption_values = self._data_processor.eliminate_off_values_from_each_appliance(house_with_appliances, off_values)
        sigmoid_values = self._data_processor.determine_sigmoid_values_for_each_appliance(all_consumption_values)
        
        bin_edges = np.arange(0.2, 0.9, 0.1)
        bin_labels = [f"{edge:.1f}-{edge+0.1:.1f}" for edge in bin_edges[:-1]]

        counts: dict[str, np.ndarray] = {}
        for appliance_name, values in sigmoid_values.items():
            counts[appliance_name], _ = np.histogram(values, bins=bin_edges)
        return bin_labels, counts

    def plot_sigmoid_distribution_bins(self, house_with_appliances: HouseWithAppliancesConsumption, off_values: dict[str, np.ndarray]) -> None:
        bin_labels, counts = self.gather_labels_and_counts(house_with_appliances, off_values)
        for _, count in counts.items():
            go.Figure(data=[go.Bar(x=bin_labels, y=count)]).show()

    def determine_top_margin_for_sigmoid(self, sigmoid_values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        filtered_sigmoid_values: dict[str, np.ndarray] = {}
        
        for appliance_name, values in sigmoid_values.items():
            threshold = np.percentile(values, self.data_percentile)
            filtered_values = values[values <= threshold]
            filtered_sigmoid_values[appliance_name] = filtered_values

        return filtered_sigmoid_values
