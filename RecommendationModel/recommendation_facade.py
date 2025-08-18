from RecommendationModel.recommendation_based_on_sigmoid_threshold import RecommendationModel
from RecommendationModel.recommendation_analytics import RecommendationAnalytics
from RecommendationModel.recommendation_plotter import RecommendationPlotter

class RecommendationFacade:
    def __init__(self) -> None:
        self.recommendation_model: RecommendationModel = RecommendationModel()
        self.analytics: RecommendationAnalytics = RecommendationAnalytics()
        self.plotter: RecommendationPlotter = RecommendationPlotter()

    def generate_recommendations(self, house_with_appliances, appliance_thresholds) -> dict[int,int]:
        return self.recommendation_model.give_recommendation_based_on_sigmoid_threshold(house_with_appliances, appliance_thresholds)

    def get_recommendation_percentage(self, house_with_appliances, appliance_thresholds) -> float:
        return self.analytics.make_percentage_of_overall_recommendations(house_with_appliances, appliance_thresholds)

    def get_hourly_recommendation_data(self, house_with_appliances, appliance_thresholds) -> tuple[dict, dict]:
        return self.recommendation_model.see_hour_distribution_per_given_recommendation(house_with_appliances, appliance_thresholds)

    def get_hourly_recommendation_percentages(self, house_with_appliances, appliance_thresholds) -> dict[int, float]:
        return self.analytics.make_dictionary_of_recommendations_percentages_per_hour(house_with_appliances, appliance_thresholds)

    def get_appliance_recommendation_counts(self, house_with_appliances, appliance_thresholds) -> dict[str, int]:
        return self.recommendation_model.see_how_many_recommendations_are_going_to_be_made(house_with_appliances, appliance_thresholds)

    def get_appliance_recommendation_percentages(self, house_with_appliances, appliance_thresholds) -> dict[str, float]:
        return self.analytics.make_percentage_of_recommendations_per_appliance(house_with_appliances, appliance_thresholds)

    def visualize_hourly_recommendations(self, house_with_appliances, appliance_thresholds) -> None:
        hourly_percentages = self.get_hourly_recommendation_percentages(house_with_appliances, appliance_thresholds)
        self.plotter.plot_hours_recommendation_histogram(hourly_percentages)

    def visualize_appliance_recommendations(self, house_with_appliances, appliance_thresholds) -> None:
        appliance_percentages = self.get_appliance_recommendation_percentages(house_with_appliances, appliance_thresholds)
        self.plotter.plot_percentage_of_recommendation_per_appliance(appliance_percentages)