import numpy as np
import plotly.graph_objects as go
from .house_with_appliances import HouseWithAppliancesConsumption
from .consumption_data_processor import ConsumptionDataProcessor

class SigmoidAnalyzer:
    def __init__(self) -> None:
        self.top_threshold = 20
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
        for appliance_name in counts:
            go.Figure(data=[go.Bar(x=bin_labels, y=counts[appliance_name])]).show()

    def _delete_big_value_labels_from_bins(self, house_with_appliances: HouseWithAppliancesConsumption, sigmoid_values: dict[str, np.ndarray], off_values) -> tuple[list[str], dict]:
        bin_labels, counts = self.gather_labels_and_counts(house_with_appliances, off_values)
        
        total_values = sum(len(values) for values in sigmoid_values.values())
        
        bins_to_remove: list[str] = []
        cumulative_percentage = 0
        
        for i in reversed(range(len(bin_labels))):
            bin_total = sum(counts[appliance][i] for appliance in counts)
            percentage = (bin_total / total_values) * 100
            
            if cumulative_percentage + percentage <= self.top_threshold:
                bins_to_remove.append(bin_labels[i])
                cumulative_percentage += percentage
            else:
                break

        filtered_labels = [label for label in bin_labels if label not in bins_to_remove]
        filtered_counts: dict[str, np.ndarray] = {}
        
        for appliance in counts:
            filtered_counts[appliance] = [
                counts[appliance][i] for i, label in enumerate(bin_labels) 
                if label not in bins_to_remove
            ]
        
        return filtered_labels, filtered_counts

    def determine_top_margin_for_sigmoid(self, house_with_appliances: HouseWithAppliancesConsumption, sigmoid_values: dict[str, np.ndarray], off_values) -> dict[str, np.ndarray]:
        bin_labels, _ = self._delete_big_value_labels_from_bins(house_with_appliances, sigmoid_values, off_values)
        top_margin = float(bin_labels[-1].split("-")[1])

        filtered_sigmoid_values: dict[str, np.ndarray] = {}
        for appliance_name, values in sigmoid_values.items():
            filtered_values = np.array([value for value in values if value <= top_margin])
            filtered_sigmoid_values[appliance_name] = filtered_values

        return filtered_sigmoid_values
