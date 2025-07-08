from SelfConsumptionModel.determine_self_consumption import SelfConsumption
class SelfSufficiency(SelfConsumption):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.self_sufficiency = None
    
    def determine_self_sufficiency_over_time(self, month=None, day=None):
        self.self_sufficiency=self.determine_self_consumption_over_time(month, day, use_load=True)