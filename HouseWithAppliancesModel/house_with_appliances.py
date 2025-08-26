from HouseModel.house import House

class HouseWithAppliancesConsumption(House):
    def __init__(self, house_id: int) -> None:
        super().__init__(house_id)
        self.appliance_consumption: dict[str, dict[str, float]] = {}

    def add_appliance_consumption(self, timestamp: str, appliance_type: str, consumption_value: float) -> None:
        self.appliance_consumption.setdefault(appliance_type, {})[timestamp] = consumption_value
