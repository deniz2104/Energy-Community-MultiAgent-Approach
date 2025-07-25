class House():
    def __init__(self, house_id):
        self.house_id = house_id
        self.consumption = {}
    def add_consumption(self, timestamp, consumption_value):
        self.consumption[timestamp] = consumption_value