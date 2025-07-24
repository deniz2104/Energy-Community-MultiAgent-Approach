import numpy as np
from sklearn.preprocessing import MinMaxScaler
class DetermineWhichApplianceConsumesMore:
    def __init__(self):
        pass
    
    def _gather_all_appliances_consumption_from_all_houses(self, appliance):
        all_consumption_values= []
        for _, consumption in appliance.appliance_consumption.items():
            for _, value in consumption:
                all_consumption_values.append(value)
        return np.unique(np.trim_zeros(np.sort(np.array(all_consumption_values))))

    def _eliminate_off_values_from_consumption_list(self,appliance,off_values):
        all_consumption_values=self.gather_all_appliances_consumption_from_all_houses(appliance)
        indices = np.where(np.isin(all_consumption_values, off_values))[0]
        all_consumption_values = np.delete(all_consumption_values, indices)
        return all_consumption_values

    def _sigmoid(self, x): return 1 / (1 + np.exp(-x))

    def _determine_sigmoid_values(self, all_consumption_values):
        scaler = MinMaxScaler(feature_range=(-1, 1))
        all_consumption_values = scaler.fit_transform(all_consumption_values.reshape(-1, 1)).flatten()
        return self._sigmoid(all_consumption_values)

    def show_sigmoid_values_along_with_consumption_values(self, appliance):
        all_consumption_values = self._gather_all_appliances_consumption_from_all_houses(appliance)
        sigmoid_values = self._determine_sigmoid_values(all_consumption_values)
        sigmoid_values = self._determine_sigmoid_values(all_consumption_values)
        for consumption, sigmoid in zip(all_consumption_values, sigmoid_values):
            print(f"Consumption: {consumption}, Sigmoid: {sigmoid}")

        
    def determine_appliances(self, appliance, off_values):
        all_consumption_values = self._gather_all_appliances_consumption_from_all_houses(appliance)
        all_consumption_values = self._eliminate_off_values_from_consumption_list(appliance, off_values)
        sigmoid_values = self._determine_sigmoid_values(all_consumption_values)
        if len(appliance.appliance_consumption.keys()) == 1:
            return list(appliance.appliance_consumption.keys())[0]
        appliances_list = []
        for appliance_name, consumption in appliance.appliance_consumption.items():
            count = 0
            for _, value in consumption:
                if value in all_consumption_values:
                    index = np.where(all_consumption_values == value)[0][0]
                    sigmoid_value = sigmoid_values[index]
                    if sigmoid_value > 0.3:
                        count += 1
            if count > len(consumption)//2:
                appliances_list.append(appliance_name)
        return appliances_list