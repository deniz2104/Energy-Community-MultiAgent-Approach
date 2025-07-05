import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from house import House

class Appliance(House):
    def __init__(self,house_id):
        super().__init__(house_id)
        self.consumption = {}

    def add_appliance_consumption(self, timestamp, appliance_type, value):
        self.consumption.setdefault(appliance_type, []).append((timestamp, value))
