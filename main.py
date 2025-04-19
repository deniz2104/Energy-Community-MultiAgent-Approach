from housebuilder import HouseBuilder
from house import House
from solar_radiation_house import SolarRadiationHouse
from solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated_builder import PowerEstimatedBuilder
from determine_self_consumption import SelfConsumption
from determine_self_sufficiency import SelfSufficiency
from determine_self_consumption_builder import SelfConsumptionBuilder
from power_estimated import PowerEstimator

if __name__ == "__main__":
    house_builder = HouseBuilder()
    houses = house_builder.build('houses_after_filtering_and_matching_with_weather_data.csv')

    solar_radiation_house_builder = SolarRadiationHouseBuilder()
    solar_radiation_house = solar_radiation_house_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    
    power_estimated_builder = PowerEstimatedBuilder()
    power_estimated = power_estimated_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    power_dict = {house.house_id: house for house in power_estimated}
    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption =[]

    for house in houses:
            sc= SelfConsumption(house.house_id)
            sc.consumption = house.consumption
            sc.power_estimated = power_dict[house.house_id].power_estimated
            sc.determine_self_consumption_over_time()
            self_consumption.append(sc)
    for self_consumption_house in self_consumption:
        print(f"House ID: {self_consumption_house.house_id}, Self Consumption: {self_consumption_house.self_consumption}")

        