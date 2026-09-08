from HouseModel.house import House
from HouseModel.house_transforms import remove_houses_having_zero_for_a_period_of_time
from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse\

_houses = House.get_instances()

def filtrate_solar_radiation_houses_by_number_of_values(solar_radiation_houses: list[SolarRadiationHouse], threshold: float = 0.95) -> list[SolarRadiationHouse]:
    for house in solar_radiation_houses:
        if len(house.solar_radiation) >= threshold * len(consumption_house.consumption):
                filtered_solar_radiation_houses.append(house)
            else:
                print(f"House {house.house_id} has less than {threshold} values and will be removed.")
        return filtered_solar_radiation_houses

    def filtrate_solar_radiation_houses_having_zeros_for_a_period_of_time(self, solar_radiation_houses: list[SolarRadiationHouse], consumption_houses: list[House]) -> list[SolarRadiationHouse]:
        consumption_dict = {house.house_id: house for house in consumption_houses}
        filtered_solar_radiation_houses: list[SolarRadiationHouse] = []

        for house in solar_radiation_houses:
            consumption_house = consumption_dict[house.house_id]
            zero_count = remove_houses_having_zero_for_a_period_of_time(consumption_house)
            if zero_count == 0:
                filtered_solar_radiation_houses.append(house)
        return filtered_solar_radiation_houses
