from house import House
from power_estimated import PowerEstimator
class SelfConsumption(House, PowerEstimator):

    def __init__(self,house_id):
        House.__init__(self,house_id)
        PowerEstimator.__init__(self,house_id)
        self.self_consumption= {}
    
    def determine_self_consumption_over_time(self,month=None, day=None,use_load=False):
        if month is None and day is None:
            p_prod = list(self.power_estimated.values())
            p_load = list(self.consumption.values())
        elif month is not None and day is None:
            p_prod = [v for k, v in self.power_estimated.items() if k.month == month]
            p_load = [v for k, v in self.consumption.items() if k.month == month]
        elif month is None and day is not None:
            p_prod = [v for k, v in self.power_estimated.items() if k.day == day]
            p_load = [v for k, v in self.consumption.items() if k.day == day]
        else:
            p_prod = [v for k, v in self.power_estimated.items() if k.month == month and (day is None or k.day == day)]
            p_load = [v for k, v in self.consumption.items() if k.month == month and (day is None or k.day == day)]
        numerator = sum(min(p_prod[i], p_load[i]) for i in range(len(p_prod)))
        denominator = sum(p_load) if use_load else sum(p_prod)
        self.self_consumption = numerator / denominator if denominator != 0 else 0
        return self.self_consumption
