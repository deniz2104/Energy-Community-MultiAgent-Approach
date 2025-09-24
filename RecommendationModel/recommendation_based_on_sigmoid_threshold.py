import pandas as pd
from ConsumptionProcessingModel.consumption_data_processor import ConsumptionDataProcessor
from HelperFiles.hours_for_day_and_night import TOTAL_HOURS
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption

class RecommendationModel:
    def __init__(self) -> None:
        self.threshold :int = 0
        self.data_processor = ConsumptionDataProcessor()

    def make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(self,house_with_appliances: HouseWithAppliancesConsumption) -> dict[str,dict[float, float]]:
        consumption_for_each_appliance= self.data_processor.gather_consumption_values_for_each_appliance(house_with_appliances)
        sigmoid_values_for_each_appliance= self.data_processor.determine_sigmoid_values_for_each_appliance(consumption_for_each_appliance)
        consumption_mapped_to_sigmoid_values = {}
        for appliance_name, _ in consumption_for_each_appliance.items():
            if appliance_name not in consumption_mapped_to_sigmoid_values:
                consumption_mapped_to_sigmoid_values[appliance_name] = dict(zip(consumption_for_each_appliance[appliance_name], sigmoid_values_for_each_appliance[appliance_name]))
        return consumption_mapped_to_sigmoid_values

    def see_how_many_recommendations_are_going_to_be_made(self, house_with_appliances : HouseWithAppliancesConsumption, appliance_thresholds :dict[str, float]) -> dict[str, int]:
        consumption_mapped_to_sigmoid_values = self.make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(house_with_appliances)
        number_of_recommendations = {}
        for appliance_name, consumption_dict in consumption_mapped_to_sigmoid_values.items():
            for _, sigmoid_value in consumption_dict.items():
                if sigmoid_value >= appliance_thresholds.get(appliance_name, 0):
                    number_of_recommendations[appliance_name] = number_of_recommendations.get(appliance_name, 0) + 1
        return number_of_recommendations

    def get_timestamp(self, house_with_appliances: HouseWithAppliancesConsumption) -> list[str]:

        first_appliance = next(iter(house_with_appliances.appliance_consumption.values()))
        return list(first_appliance.keys())

    def set_threshold(self, appliance_thresholds: dict[str, float]) -> None:
        self.threshold = len(appliance_thresholds) // 2 + len(appliance_thresholds) % 2

    def set_timestamp(self, house_with_appliances: HouseWithAppliancesConsumption) -> list[str]:
        return self.get_timestamp(house_with_appliances)

    def set_dictionary_of_consumption_along_with_sigmoid(self, house_with_appliances: HouseWithAppliancesConsumption) -> dict[str, dict[float, float]]:
        return self.make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(house_with_appliances)

    def _count_appliances_values_above_threshold(self, timestamp: str, house_with_appliances: HouseWithAppliancesConsumption, appliance_thresholds: dict[str, float], dictionary_of_consumption_along_with_sigmoid: dict[str, dict[float, float]]) -> int:
        count_of_appliances = 0
        for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
            consumption_value = consumption.get(timestamp, 0)
            sigmoid_value = dictionary_of_consumption_along_with_sigmoid[appliance_type].get(consumption_value, 0)
            
            if sigmoid_value >= appliance_thresholds.get(appliance_type, 0):
                count_of_appliances += 1
        return count_of_appliances

    def give_recommendation_based_on_sigmoid_threshold(self, house_with_appliances, appliance_thresholds):
        whole_timestamp = self.set_timestamp(house_with_appliances)
        self.set_threshold(appliance_thresholds)
        dictionary_of_consumption_along_with_sigmoid = self.set_dictionary_of_consumption_along_with_sigmoid(house_with_appliances)
        recommendation_dictionary: dict[int, int] = {}
        count=0

        for timestamp in whole_timestamp:
            count_of_appliances = self._count_appliances_values_above_threshold(
                timestamp, house_with_appliances, appliance_thresholds, dictionary_of_consumption_along_with_sigmoid
            )
                    
            if count_of_appliances >= self.threshold:
                recommendation_dictionary[count] = 1
            else : recommendation_dictionary[count] = 0
            count += 1
            
        return recommendation_dictionary

    def see_hour_distribution_per_given_recommendation(self, house_with_appliances: HouseWithAppliancesConsumption, appliance_thresholds: dict[str, float]) -> tuple[dict[int, int], dict[int, int]]:
        hour_distribution = {hour: 0 for hour in range(TOTAL_HOURS)}
        total_hour_distribution = {hour: 0 for hour in range(TOTAL_HOURS)}
        
        whole_timestamp = self.set_timestamp(house_with_appliances)
        dictionary_of_consumption_along_with_sigmoid = self.set_dictionary_of_consumption_along_with_sigmoid(house_with_appliances)
        self.set_threshold(appliance_thresholds)

        for timestamp in whole_timestamp:
            hour = pd.to_datetime(timestamp).hour
            total_hour_distribution[hour] += 1
            
            count_of_appliances = self._count_appliances_values_above_threshold(
                timestamp, house_with_appliances, appliance_thresholds, dictionary_of_consumption_along_with_sigmoid
            )

            if count_of_appliances >= self.threshold:
                hour_distribution[hour] += 1

        return total_hour_distribution, hour_distribution