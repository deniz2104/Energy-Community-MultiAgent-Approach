from file_to_handle_absolute_path_imports import *
from HouseWithAppliancesModel.house_with_appliances_builder import HouseWithAppliancesBuilder
appliance_builder = HouseWithAppliancesBuilder()
appliances = appliance_builder.build("CSVs/appliance_consumption_preprocessed.csv")
appliance_types = set()
for appliance in appliances:
    appliance_types.update(list(appliance.appliance_consumption.keys()))
