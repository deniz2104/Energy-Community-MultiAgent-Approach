from housebuilder import HouseBuilder
from solar_radiation_house import SolarRadiationHouse
class SolarRadiationHouseBuilder(HouseBuilder) :
    def __init__(self):
        super().__init__()
    def build(self, csv_path):
        solar_radiation_houses = {}
        rows=super().open_csv_file(csv_path)

        for house_id, timestamp, value in rows:
            if house_id not in solar_radiation_houses:
                solar_radiation_houses[house_id] = SolarRadiationHouse(house_id)
            solar_radiation_houses[house_id].add_solar_radiation(timestamp, value)
        return list(solar_radiation_houses.values())
    
    def match_and_filter_solar_houses(self,solar_houses, consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for solar_house in solar_houses:
            if solar_house.house_id in consumption_dict:
                consumption_house = consumption_dict[solar_house.house_id]
                solar_house.change_timing_for_solar_radiation(consumption_house)
            else:
                print(f"No matching consumption data for solar house {solar_house.house_id}")