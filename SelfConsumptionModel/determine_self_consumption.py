from typing import Optional
from PowerEstimatedModel.power_estimated import PowerEstimator

class SelfConsumption(PowerEstimator):
    def __init__(self, house_id: int) -> None:
        super().__init__(house_id)
        self.self_consumption: float = 0.0

    def determine_self_consumption_over_time(self,specified_value_range: Optional[int] = None, use_load: bool = False) -> float:

        p_prod = list(self.power_estimated.values())
        p_load = list(self.consumption.values())

        values_range=min(len(p_prod),len(p_load),specified_value_range) if specified_value_range is not None else min(len(p_prod),len(p_load))

        numerator = sum(min(p_prod[i], p_load[i]) for i in range(values_range))
        denominator = sum(p_load[i] for i in range(values_range)) if use_load else sum(p_prod[i] for i in range(values_range))
        result = numerator / denominator if denominator != 0 else 0
        self.self_consumption = result
        return result
