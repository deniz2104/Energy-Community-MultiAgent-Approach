from HouseWithAppliancesModel.consumption_data_processor import ConsumptionDataProcessor
from RecommendationModel.recommendation_based_on_sigmoid_threshold import RecommendationModel

class RecommendationAnalytics:
    def __init__(self) -> None:
        self._recommendation_model = RecommendationModel()
        self._data_processor = ConsumptionDataProcessor()

    def make_percentage_of_overall_recommendations(self, house_with_appliances, appliance_thresholds) -> float:
        recommendation_dictionary = self._recommendation_model.give_recommendation_based_on_sigmoid_threshold(house_with_appliances, appliance_thresholds)
        total_timestamps = len(self._recommendation_model.get_timestamp(house_with_appliances))

        number_of_recommendations = sum(recommendation_dictionary.values())
        
        return (number_of_recommendations / total_timestamps) * 100

    def make_dictionary_of_recommendations_percentages_per_hour(self, house_with_appliances, appliance_thresholds) -> dict[int, float]:
        total_hour_distribution, hour_distribution = self._recommendation_model.see_hour_distribution_per_given_recommendation(house_with_appliances, appliance_thresholds)

        return {
            hour: (count / total_hour_distribution[hour] * 100) if total_hour_distribution[hour] > 0 else 0
            for hour, count in hour_distribution.items()
        }

    def make_percentage_of_recommendations_per_appliance(self, house_with_appliances, appliance_thresholds) -> dict[str, float]:
        number_of_recommendations = self._recommendation_model.see_how_many_recommendations_are_going_to_be_made(house_with_appliances, appliance_thresholds)
        percentage_of_recommendations = {}
        consumption_for_each_appliance = self._data_processor.gather_consumption_values_for_each_appliance(house_with_appliances)
        for appliance_name, _ in consumption_for_each_appliance.items():
            total_consumption = len(consumption_for_each_appliance[appliance_name])
            if total_consumption > 0:
                percentage_of_recommendations[appliance_name] = (number_of_recommendations.get(appliance_name, 0) / total_consumption) * 100
        return percentage_of_recommendations