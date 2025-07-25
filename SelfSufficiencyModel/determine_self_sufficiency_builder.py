from .determine_self_sufficiency import SelfSufficiency
from HouseModel.house import House
from PowerEstimatedModel.power_estimated import PowerEstimator

class SelfSufficiencyBuilder():
    def __init__(self) -> None:
        pass

    def build_self_sufficiency(self, houses: list[House], power_estimated_houses: list[PowerEstimator]) -> list[SelfSufficiency]:
        self_sufficiency_houses: dict[int, SelfSufficiency] = {}
        power_dict = {house.house_id: house for house in power_estimated_houses}
        for house in houses:
            self_sufficiency_houses[house.house_id] = SelfSufficiency(house.house_id)
            self_sufficiency_houses[house.house_id].consumption = house.consumption
            self_sufficiency_houses[house.house_id].power_estimated = power_dict[house.house_id].power_estimated
            self_sufficiency_houses[house.house_id].determine_self_sufficiency_over_time()
        return list(self_sufficiency_houses.values())