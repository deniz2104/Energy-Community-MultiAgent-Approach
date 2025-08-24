from typing import Optional
from SelfConsumptionModel.determine_self_consumption import SelfConsumption

class SelfSufficiency(SelfConsumption):
    def __init__(self, house_id) -> None:
        super().__init__(house_id)
        self.self_sufficiency: float = 0.0

    def determine_self_sufficiency_over_time(self, month: Optional[int] = None, day: Optional[int] = None) -> None:
        self.self_sufficiency = self.determine_self_consumption_over_time(month, day, use_load=True)