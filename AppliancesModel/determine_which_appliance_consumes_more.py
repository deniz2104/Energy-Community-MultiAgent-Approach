import numpy as np
from sklearn.preprocessing import MinMaxScaler
class DetermineWhichApplianceConsumesMore:
    def __init__(self):
        pass
    
    ##TODO: trebuie sa gasesc un threshold care are legatura in particular cu casa respectiva, trebuie sa generalizez thresold ul pe care il iau
    def gather_all_appliances_consumption_from_all_houses(self, appliance):
        all_consumption_values= []
        for _, consumption in appliance.appliance_consumption.items():
            for _, value in consumption:
                all_consumption_values.append(value)
        return np.sort(np.array(all_consumption_values))


    def sigmoid(self, x): return 1 / (1 + np.exp(-x))

    def determine_sigmoid_values(self, all_consumption_values):
        scaler = MinMaxScaler(feature_range=(-1, 1))
        all_consumption_values = scaler.fit_transform(all_consumption_values.reshape(-1, 1)).flatten()
        return self.sigmoid(all_consumption_values)

    def show_sigmoid_values_along_with_consumption_values(self, appliance):
        all_consumption_values = self.gather_all_appliances_consumption_from_all_houses(appliance)
        sigmoid_values = self.determine_sigmoid_values(all_consumption_values)
        for consumption, sigmoid in zip(all_consumption_values, sigmoid_values):
            print(f"Consumption: {consumption}, Sigmoid: {sigmoid}")
