from .determine_self_sufficiency import SelfSufficiency
class SelfSufficiencyBuilder():
    def __init__(self):
        pass

    def build_self_sufficiency(self, houses,power_estimated_houses):
        self_sufficiency_houses = {}
        power_dict = {house.house_id: house for house in power_estimated_houses}
        for house in houses:
            self_sufficiency_houses[house.house_id] = SelfSufficiency(house.house_id)
            self_sufficiency_houses[house.house_id].consumption = house.consumption
            self_sufficiency_houses[house.house_id].power_estimated = power_dict[house.house_id].power_estimated
            self_sufficiency_houses[house.house_id].determine_self_sufficiency_over_time()
        return list(self_sufficiency_houses.values())