from solar_radiation_house import SolarRadiationHouse
f=0.8
Pmax=575
GTSTC=1000

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.power_estimated = {}
    def add_power_estimated(self,timestamp,value):
        self.power_estimated[timestamp] = Pmax * f * (value / GTSTC)
    
    def plot_power_over_time_for_a_numer_of_panels(self,number,month=None, day=None):
        temp_radiation = self.solar_radiation
        self.power_estimated = {key: value * number for key, value in self.power_estimated.items()}
        self.solar_radiation = self.power_estimated
        super().plot_consumption_over_time(month, day)
        self.solar_radiation = temp_radiation

    def plot_power_over_time_range_for_a_number_of_panels(self,number,time_stamp_1, time_stamp_2):
        temp_radiation = self.solar_radiation
        self.solar_radiation = self.power_estimated
        self.power_estimated = {key: value * number for key, value in self.power_estimated.items()}
        super().plot_consumption_over_time_range(time_stamp_1, time_stamp_2)
        self.solar_radiation = temp_radiation