from typing import Optional, List
from PowerEstimatedModel.power_estimated import PowerEstimator
from HelperFiles.file_to_handle_absolute_path_imports import *

class SelfConsumption(PowerEstimator):
    def __init__(self, house_id: int) -> None:
        super().__init__(house_id)
        self.self_consumption: Optional[float] = None
    
    def determine_self_consumption_over_time(self, month: Optional[int] = None, day: Optional[int] = None, use_load: bool = False) -> float:
        if month is None and day is None:
            p_prod: List[float] = list(self.power_estimated.values())
            p_load: List[float] = list(self.consumption.values())
        elif month is not None and day is None:
            p_prod = [v for k, v in self.power_estimated.items() if k.month == month]
            p_load = [v for k, v in self.consumption.items() if k.month == month]
        elif month is None and day is not None:
            p_prod = [v for k, v in self.power_estimated.items() if k.day == day]
            p_load = [v for k, v in self.consumption.items() if k.day == day]
        else:
            p_prod = [v for k, v in self.power_estimated.items() if k.month == month and (day is None or k.day == day)]
            p_load = [v for k, v in self.consumption.items() if k.month == month and (day is None or k.day == day)]
        numerator = sum(min(p_prod[i], p_load[i]) for i in range(min(len(p_prod), len(p_load))))
        denominator = sum(p_load) if use_load else sum(p_prod)
        result = numerator / denominator if denominator != 0 else 0
        self.self_consumption = result
        return result
