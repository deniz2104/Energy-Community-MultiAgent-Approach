from housebuilder import HouseBuilder
from solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated_builder import PowerEstimatedBuilder
from determine_self_consumption_builder import SelfConsumptionBuilder
from determine_self_sufficiency_builder import SelfSufficiencyBuilder

if __name__ == "__main__":
    house_builder = HouseBuilder()
    houses = house_builder.build('houses_after_filtering_and_matching_with_weather_data.csv')

    solar_radiation_house_builder = SolarRadiationHouseBuilder()
    solar_radiation_house = solar_radiation_house_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    
    power_estimated_builder = PowerEstimatedBuilder()
    power_estimated = power_estimated_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    
    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption = self_consumption_builder.build_self_consumption(houses, power_estimated)

    self_sufficiency_builder = SelfSufficiencyBuilder()
    self_sufficiency_house = self_sufficiency_builder.build_self_sufficiency(houses, power_estimated)

        