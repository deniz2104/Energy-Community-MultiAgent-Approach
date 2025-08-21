from HouseModel.house_facade import HouseFacade
from SolarRadiationModel.solar_radiation_house_facade import SolarRadiationHouseFacade
from PowerEstimatedModel.power_estimated_facade import PowerEstimatedFacade
from SelfConsumptionModel.determine_self_consumption_builder import SelfConsumptionBuilder
from SelfSufficiencyModel.determine_self_sufficiency_builder import SelfSufficiencyBuilder
from HouseWithAppliancesModel.house_with_appliances_facade import HouseWithAppliancesFacade
from RecommendationModel.recommendation_facade import RecommendationFacade
from AgentModel.house_model import HouseModel

## de facut plot in folderul AgentModel + type hints in tot folderul
## ca sa vizualizez rezultatele, reprezentam consumul estimat in timp, productia estimata in timp, consumul simulat in timp (pe acelasi grafic),un calcul de autoconsum simulat/estimat, la fel si autonomie si recomandarile pe un grafic separat(bar chart)
## la final ar fi good practice sa fac un devcontainer

if __name__ == "__main__":
    house_facade = HouseFacade()
    houses = house_facade.build_houses("CSVs/houses_after_filtering_and_matching_with_weather_data.csv")
    
    solar_radiation_house_facade = SolarRadiationHouseFacade()
    solar_radiation_houses = solar_radiation_house_facade.builder.build("CSVs/solar_radiation_after_resampling_and_matching_houses.csv")

    power_estimated_facade = PowerEstimatedFacade()
    power_estimated = power_estimated_facade.build_power_estimated_data('CSVs/solar_radiation_after_resampling_and_matching_houses.csv')
    power_estimated_facade.determine_NEEG_for_all_houses(power_estimated)

    power_estimated_dict = {pe.house_id: pe for pe in power_estimated}
    for house in houses:
        if house.house_id in power_estimated_dict:
            house.power_estimated = power_estimated_dict[house.house_id].power_estimated

    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption = self_consumption_builder.build_self_consumption(houses, power_estimated)
    
    self_sufficiency_builder = SelfSufficiencyBuilder()
    self_sufficiency_house = self_sufficiency_builder.build_self_sufficiency(houses, power_estimated)

    house_with_appliances_facade = HouseWithAppliancesFacade()
    houses_with_appliances = house_with_appliances_facade.builder.build("CSVs/appliance_consumption_preprocessed.csv")
    
    recommendation_model_facade = RecommendationFacade()
    recommendation_dictionaries = {}
    
    for house in houses_with_appliances[:1]:
        appliances_thresholds = house_with_appliances_facade.determine_appliance_thresholds(house)
        recommendation_dict = recommendation_model_facade.generate_recommendations(house, appliances_thresholds)
        recommendation_dictionaries[house.house_id] = recommendation_dict
        
    agent_model = HouseModel(n=1, house_obj=houses[:1], recommendation_dictionaries=recommendation_dictionaries)

    simulation_steps = 168