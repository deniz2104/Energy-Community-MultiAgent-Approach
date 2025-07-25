from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.power_estimated = {}
        self.NEEG= None
        self.f = 0.8
        self.GTSTC= 1000
    
    def add_power_estimated(self,timestamp,solar_radiatian_value,Pmax=575, number_of_panels=1):
        self.power_estimated[timestamp] = Pmax * self.f *number_of_panels * (solar_radiatian_value / self.GTSTC)

    def determine_NEEG(self):
        self.NEEG = sum(
            min(self.power_estimated[ts], self.consumption[ts])
            for ts in self.power_estimated
        )