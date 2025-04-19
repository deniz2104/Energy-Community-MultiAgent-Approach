from determine_self_consumption import SelfConsumption
class SelfConsumptionBuilder:
    def __init__(self):
        pass
    def build_self_consumption(self,houses):
        self_consumption_house ={}
        for house in houses:
            if(house.house_id not in self_consumption_house):
                self_consumption_house[house.house_id] = SelfConsumption(house.house_id)
                self_consumption_house[house.house_id].determine_self_consumption_over_time()
        return list(self_consumption_house.values())