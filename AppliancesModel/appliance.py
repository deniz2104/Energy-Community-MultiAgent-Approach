from house import House
from HelperFiles.file_to_handle_absolute_path_imports import *

class Appliance(House):
    def __init__(self,house_id):
        super().__init__(house_id)
        self.appliance_consumption = {}

    def add_appliance_consumption(self, timestamp, appliance_type, value):
        self.appliance_consumption.setdefault(appliance_type, []).append((timestamp, value))
