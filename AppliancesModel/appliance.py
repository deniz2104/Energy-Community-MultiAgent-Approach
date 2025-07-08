import sys
import os
from house import House
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Appliance(House):
    def __init__(self,house_id):
        super().__init__(house_id)
        self.appliance_consumption = {}

    def add_appliance_consumption(self, timestamp, appliance_type, value):
        self.appliance_consumption.setdefault(appliance_type, []).append((timestamp, value))
