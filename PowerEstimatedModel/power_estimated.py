from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.power_estimated = {}
        self.NEEG= None
    
    def add_power_estimated(self,timestamp,value,Pmax=575 , GTSTC=1000, number_of_panels=1, f=0.8):
        self.power_estimated[timestamp] = Pmax * f *number_of_panels * (value / GTSTC)

    def determine_NEEG(self):
        self.NEEG = sum(
            min(self.power_estimated[ts], self.consumption[ts])
            for ts in self.power_estimated
        )