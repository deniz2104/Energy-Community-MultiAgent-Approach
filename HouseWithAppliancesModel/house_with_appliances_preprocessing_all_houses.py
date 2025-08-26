from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption
from HouseWithAppliancesModel.house_with_appliances_preprocessing_data import HouseWithAppliancesPreprocessingData
from HouseModel.house import House

class HouseWithAppliancesPreprocessingAllHouses:
    def __init__(self) -> None:
        self.preprocessing_data = HouseWithAppliancesPreprocessingData()

    def remove_appliances_with_zero_data(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> None:
        for house in houses_with_appliances:
            self.preprocessing_data.eliminate_appliances_with_lot_of_zeros_consumption(house)

    def eliminate_anomalies_in_appliances(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> None:
        for house in houses_with_appliances:
            self.preprocessing_data.eliminate_anomalies_in_my_data(house)

    def eliminate_appliances_with_five_days_of_no_consumption(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> None:
        for house in houses_with_appliances:
            self.preprocessing_data.eliminate_appliance_with_five_days_of_no_consumption(house)

    def matching_timestamps_between_appliance_and_house(self, house_with_appliances: list[HouseWithAppliancesConsumption], consumption_houses: list[House]) -> None:
        consumption_dict = {house.house_id: house for house in consumption_houses}

        for house in house_with_appliances:
            if house.house_id in consumption_dict:
                consumption_house = consumption_dict[house.house_id]
                self.preprocessing_data.eliminate_days_after_a_year(house, consumption_house)