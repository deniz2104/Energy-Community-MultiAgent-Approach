from SolarRadiationModel.solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated import PowerEstimator
class PowerEstimatedBuilder(SolarRadiationHouseBuilder):
    def __init__(self):
        pass
    def build(self,csv_path):
        power_estimated_houses ={}
        rows=super().open_csv_file(csv_path)

        for house_id, timestamp, value in rows:
            if house_id not in power_estimated_houses:
                power_estimated_houses[house_id] = PowerEstimator(house_id)
            power_estimated_houses[house_id].add_consumption(timestamp,value)
            power_estimated_houses[house_id].add_power_estimated(timestamp, value)
        return list(power_estimated_houses.values())
    
    def determine_NEEG_for_all_houses(self, power_estimated):
        for house in power_estimated:
            house.determine_NEEG()
