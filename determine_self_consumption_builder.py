from determine_self_consumption import SelfConsumption
class SelfConsumptionBuilder():
    def __init__(self):
        pass
    def build_self_consumption(self,houses,power_estimated_houses):
        self_consumption_house ={}
        power_dict={house.house_id: house for house in power_estimated_houses}
        for house in houses:
            self_consumption_house[house.house_id] = SelfConsumption(house.house_id)
            self_consumption_house[house.house_id].consumption = house.consumption
            self_consumption_house[house.house_id].power_estimated = power_dict[house.house_id].power_estimated
            self_consumption_house[house.house_id].determine_self_consumption_over_time()
        return list(self_consumption_house.values())