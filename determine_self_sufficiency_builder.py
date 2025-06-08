from determine_self_sufficiency import SelfSufficiency

class SelfSufficiencyBuilder:
    def __init__(self):
        pass

    def build_self_sufficiency(self, houses):
        self_sufficiency_house = {}
        for house in houses:
            self_sufficiency_house[house.house_id] = SelfSufficiency(house.house_id)
            self_sufficiency_house[house.house_id].determine_self_sufficiency_over_time()
        return list(self_sufficiency_house.values())