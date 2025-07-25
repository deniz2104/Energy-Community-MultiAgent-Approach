from typing import Optional
from SelfConsumptionModel.determine_self_consumption import SelfConsumption
class SelfSufficiency(SelfConsumption):
    def __init__(self, house_id) -> None:
        super().__init__(house_id)
        self.self_sufficiency: Optional[float] = None

    def determine_self_sufficiency_over_time(self, month=None, day=None) -> None:
        self.self_sufficiency = self.determine_self_consumption_over_time(month, day, use_load=True)