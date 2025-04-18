from solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated import PowerEstimator
class PowerEstimatedBuilder(SolarRadiationHouseBuilder):
    def __init__(self):
        pass
    def build(self,csv_path):
        power_estimated_houses ={}
        rows=super().open_csv_file("solar_radiation_after_resampling_and_matching_houses.csv")

        for house_id, timestamp, value in rows:
            if house_id not in power_estimated_houses:
                power_estimated_houses[house_id] = PowerEstimator(house_id)
            power_estimated_houses[house_id].add_power_estimated(timestamp, value)
        return list(power_estimated_houses.values())