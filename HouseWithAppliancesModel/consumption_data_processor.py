import numpy as np
from sklearn.preprocessing import MinMaxScaler
from .house_with_appliances import HouseWithAppliancesConsumption

class ConsumptionDataProcessor:
    def __init__(self) -> None:
        pass
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray: 
        return 1 / (1 + np.exp(-x))

    def _gather_consumption_values_for_each_appliance(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, np.ndarray]:
        consumption_values: dict[str, np.ndarray] = {}
        for appliance_name, consumption in house_with_appliances.appliance_consumption.items():
            values = np.array(list(consumption.values()))
            consumption_values[appliance_name] = np.unique(np.trim_zeros(np.sort(values)))
        return consumption_values

    def eliminate_off_values_from_each_appliance(self, house_with_appliances: HouseWithAppliancesConsumption, off_consumption_values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        consumption_values = self._gather_consumption_values_for_each_appliance(house_with_appliances)
        for appliance_name, values in consumption_values.items():
            if appliance_name in off_consumption_values:
                off_values_per_appliance = off_consumption_values[appliance_name]
                mask = ~np.isin(values, off_values_per_appliance)
                consumption_values[appliance_name] = values[mask]
        return consumption_values

    def determine_sigmoid_values_for_each_appliance(self, consumption_values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        sigmoid_values: dict[str, np.ndarray] = {}
        for appliance_name, values in consumption_values.items():
            scaled_values = MinMaxScaler(feature_range=(-1, 1)).fit_transform(values.reshape(-1, 1)).flatten()
            sigmoid_values[appliance_name] = self._sigmoid(scaled_values)
        return sigmoid_values
