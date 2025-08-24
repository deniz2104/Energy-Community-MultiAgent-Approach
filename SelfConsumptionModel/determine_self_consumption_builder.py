from typing import Optional
from SelfConsumptionModel.determine_self_consumption import SelfConsumption
from HouseModel.house import House
from PowerEstimatedModel.power_estimated import PowerEstimator

class SelfConsumptionBuilder():
    def __init__(self) -> None:
        pass

    def build_self_consumption(self, houses: list[House], power_estimated_houses: list[PowerEstimator],specified_value_range: Optional[int] = None) -> list[SelfConsumption]:
        self_consumption_houses: dict[int, SelfConsumption] = {}
        power_dict = {house.house_id: house for house in power_estimated_houses}
        for house in houses:
            self_consumption_houses[house.house_id] = SelfConsumption(house.house_id)
            self_consumption_houses[house.house_id].consumption = house.consumption
            self_consumption_houses[house.house_id].power_estimated = power_dict[house.house_id].power_estimated
            self_consumption_houses[house.house_id].determine_self_consumption_over_time(specified_value_range)
        return list(self_consumption_houses.values())