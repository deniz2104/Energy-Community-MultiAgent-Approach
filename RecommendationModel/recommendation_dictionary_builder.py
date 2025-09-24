from HouseWithAppliancesModel.house_with_appliances_facade import HouseWithAppliancesFacade
from ConsumptionProcessingModel.consumption_processing_facade import ConsumptionProcessingFacade
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption
from RecommendationModel.recommendation_facade import RecommendationFacade
import csv

class RecommendationDictionaryBuilder:
    def __init__(self):
        self.house_with_appliances_facade = HouseWithAppliancesFacade()
        self.consumption_processing_facade = ConsumptionProcessingFacade()
        self.recommendation_model_facade = RecommendationFacade()

    def open_csv_file(self, csv_path: str) -> list[tuple[int, int, int]]:
        results: list[tuple[int, int, int]] = []
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                step = int(row['Step'])
                recommendation = int(row['Recommendation'])
                results.append((house_id, step, recommendation))
        return results
            
    def build(self, csv_path: str) -> dict[int, dict[int,int]]:
        recommendations: dict[int, dict[int,int]] = {}
        rows = self.open_csv_file(csv_path)
        for house_id, step, recommendation in rows:
            if house_id not in recommendations:
                recommendations[house_id] = {}
            recommendations[house_id][step] = recommendation
        return recommendations

    def build_recommendation_dictionary(self, house):
        appliances_thresholds = self.consumption_processing_facade.determine_appliance_thresholds(house)
        recommendation_dict = self.recommendation_model_facade.generate_recommendations(house, appliances_thresholds)
        return recommendation_dict

    def export_to_csv(self, houses: list[HouseWithAppliancesConsumption], file_path: str) -> None:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'Step', 'Recommendation'])
            for house in houses:
                recommendation_dict = self.build_recommendation_dictionary(house)
                for step, recommendation in recommendation_dict.items():
                    writer.writerow([house.house_id, step, recommendation])