from solar_radiation_house import SolarRadiationHouse

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id):
        super().__init__(house_id)
        self.power_estimated = {}
    
    def add_power_estimated(self,timestamp,value,Pmax=575 , GTSTC=1000, number_of_panels=1, f=0.8):
        self.power_estimated[timestamp] = Pmax * f *number_of_panels * (value / GTSTC)
    
    def plot_power_over_time_for_a_numer_of_panels(self,month=None, day=None):
        temp_radiation = self.solar_radiation
        self.power_estimated = {key: value for key, value in self.power_estimated.items()}
        self.solar_radiation = self.power_estimated
        super().plot_consumption_over_time(month, day)
        self.solar_radiation = temp_radiation

    def plot_power_over_time_range_for_a_number_of_panels(self,time_stamp_1, time_stamp_2):
        temp_radiation = self.solar_radiation
        self.solar_radiation = self.power_estimated
        self.power_estimated = {key: value for key, value in self.power_estimated.items()}
        super().plot_consumption_over_time_range(time_stamp_1, time_stamp_2)
        self.solar_radiation = temp_radiation