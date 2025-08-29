from HouseModel.house_facade import HouseFacade
from SolarRadiationModel.solar_radiation_house_facade import SolarRadiationHouseFacade
from PowerEstimatedModel.power_estimated_facade import PowerEstimatedFacade
from SelfConsumptionModel.determine_self_consumption_builder import SelfConsumptionBuilder
from SelfConsumptionModel.self_consumption_attribute_adder import SelfConsumptionAttributeAdder
from SelfSufficiencyModel.determine_self_sufficiency_builder import SelfSufficiencyBuilder
from SelfSufficiencyModel.self_sufficiency_attribute_adder import SelfSufficiencyAttributeAdder
from HouseWithAppliancesModel.house_with_appliances_facade import HouseWithAppliancesFacade
from RecommendationModel.recommendation_facade import RecommendationFacade
from RecommendationModel.recommendation_dictionary_builder import RecommendationDictionaryBuilder
from AgentModel.house_model import HouseModel
from AgentModel.agent_plots import AgentPlots
from AgentModel.agent_statistics import AgentStatistics
from AgentModel.agent_maximum_simulation_steps import AgentSimulationSteps

## la final ar fi good practice sa fac un devcontainer
## caiet practica
## web scraping pentru aflarea pretului 
## pun graficele organizat intr-un keynote pt 1.5,10,15,20,23
## Desenez pe grafic linia Pareto

if __name__ == "__main__":
    house_facade = HouseFacade()
    houses = house_facade.build_houses("CSVs/houses_after_filtering_and_matching_with_weather_data.csv")
    
    solar_radiation_house_facade = SolarRadiationHouseFacade()
    solar_radiation_houses = solar_radiation_house_facade.builder.build("CSVs/solar_radiation_after_resampling_and_matching_houses.csv")

    power_estimated_facade = PowerEstimatedFacade()
    power_estimated = power_estimated_facade.build_power_estimated_data('CSVs/solar_radiation_after_resampling_and_matching_houses.csv')
    power_estimated_facade.determine_NEEG_for_all_houses(power_estimated)
    power_estimated_facade.add_power_estimated_attribute_to_houses(houses, power_estimated)

    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption = self_consumption_builder.build_self_consumption(houses, power_estimated)

    self_consumption_adder = SelfConsumptionAttributeAdder()
    self_consumption_adder.add_self_consumption_to_houses(houses, self_consumption)
    
    self_sufficiency_builder = SelfSufficiencyBuilder()
    self_sufficiency_house = self_sufficiency_builder.build_self_sufficiency(houses, power_estimated)

    self_sufficiency_adder = SelfSufficiencyAttributeAdder()
    self_sufficiency_adder.add_self_sufficiency_to_houses(houses, self_sufficiency_house)

    house_with_appliances_facade = HouseWithAppliancesFacade()
    houses_with_appliances = house_with_appliances_facade.builder.build("CSVs/appliance_consumption_preprocessed.csv")
    
    recommendation_model_facade = RecommendationFacade()
    recommendation_dictionaries = RecommendationDictionaryBuilder().build("CSVs/recommendation_dictionaries.csv")

    agent_model = HouseModel(n=5, house_obj=houses[:5], recommendation_dictionaries=recommendation_dictionaries)

    simulation_steps = AgentSimulationSteps(agent_model).get_maximum_simulation_steps(houses[:5])

    agent_statistics_model = AgentStatistics(agent_model, simulation_steps)

    agent_statistics_model.run_simulation_and_generate_statistics()
    
    agent_plots = AgentPlots(agent_model)
    
    agent_plots.plot_self_consumption_and_sufficiency_comparison()
    agent_plots.plot_self_consumption_sufficiency_scatter()