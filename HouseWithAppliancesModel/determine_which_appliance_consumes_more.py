import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from .house_with_appliances import HouseWithAppliancesConsumption
class DetermineWhichApplianceConsumesMore:
    def __init__(self) -> None:
        pass

    def _gather_all_appliances_consumption_from_a_house(self, house_with_appliances: HouseWithAppliancesConsumption) -> np.ndarray:
        all_consumption_values= []
        for _, consumption in house_with_appliances.appliance_consumption.items():
            for _, value in consumption:
                all_consumption_values.append(value)
        return np.unique(np.trim_zeros(np.sort(np.array(all_consumption_values))))

    def plot_sigmoid_distribution_bins(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        all_consumption_values = self._gather_all_appliances_consumption_from_a_house(house_with_appliances)
        sigmoid_values = self._determine_sigmoid_values(all_consumption_values)
        
        bin_edges = np.arange(0.2, 0.9, 0.1)
        bin_labels = [f"{edge:.1f}-{edge+0.1:.1f}" for edge in bin_edges[:-1]]
        
        counts, _ = np.histogram(sigmoid_values, bins=bin_edges)
        
        go.Figure(data=[go.Bar(x=bin_labels, y=counts)]).show()
        print("\nSigmoid Values Distribution by Bins:")
        total_values = len(sigmoid_values)
        for _, (label, count) in enumerate(zip(bin_labels, counts)):
            percentage = (count / total_values) * 100
            print(f"{label}: {count} values ({percentage:.2f}%)")

    def _sigmoid(self, x: np.ndarray) -> np.ndarray: return 1 / (1 + np.exp(-x))

    def _determine_sigmoid_values(self, all_consumption_values: np.ndarray) -> np.ndarray:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        all_consumption_values = scaler.fit_transform(all_consumption_values.reshape(-1, 1)).flatten()
        return self._sigmoid(all_consumption_values)

    def show_sigmoid_values_along_with_consumption_values(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        all_consumption_values = self._gather_all_appliances_consumption_from_a_house(house_with_appliances)
        sigmoid_values = self._determine_sigmoid_values(all_consumption_values)
        for consumption, sigmoid in zip(all_consumption_values, sigmoid_values):
            print(f"Consumption: {consumption}, Sigmoid: {sigmoid}")


    def determine_appliances(self, house_with_appliances: HouseWithAppliancesConsumption, threshold: float = 0.3) -> list[str]:
        all_consumption_values = self._gather_all_appliances_consumption_from_a_house(house_with_appliances)
        sigmoid_values = self._determine_sigmoid_values(all_consumption_values)
        if len(house_with_appliances.appliance_consumption.keys()) == 1:
            return list(house_with_appliances.appliance_consumption.keys())[0]
        appliances_list = []
        for appliance_name, consumption in house_with_appliances.appliance_consumption.items():
            count = 0
            for _, value in consumption:
                if value in all_consumption_values:
                    index = np.where(all_consumption_values == value)[0][0]
                    sigmoid_value = sigmoid_values[index]
                    if sigmoid_value > threshold:
                        count += 1
            if count > len(consumption)//2:
                appliances_list.append(appliance_name)
        return appliances_list