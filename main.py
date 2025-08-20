from HouseModel.house_facade import HouseFacade
from SolarRadiationModel.solar_radiation_house_facade import SolarRadiationHouseFacade
from PowerEstimatedModel.power_estimated_facade import PowerEstimatedFacade
from SelfConsumptionModel.determine_self_consumption_builder import SelfConsumptionBuilder
from SelfSufficiencyModel.determine_self_sufficiency_builder import SelfSufficiencyBuilder
from HouseWithAppliancesModel.house_with_appliances_facade import HouseWithAppliancesFacade
from RecommendationModel.recommendation_facade import RecommendationFacade
from AgentModel.house_model import HouseModel
from AgentModel.house_agent import HouseAgent
from AgentModel.manager_agent import ManagerAgent
# in solar radiation model am scris o prostie, eu nu am functia aia
# in recommendationModel nu mai stiu ce am vrut sa sciru, nu se apeleaza functile alea
# de rezolvat erori de linter in HouseModel si in RecommendationModel

## Trebuie sa generez in agent un nou profil generat
## la final ar fi good practice sa fac si un __init__.py si un devcontainer

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
    for i in range(simulation_steps):
        agent_model.step()

    house_agents: list[HouseAgent] = [agent for agent in agent_model.schedule.agents if isinstance(agent, HouseAgent)]
    manager_agents: list[ManagerAgent] = [agent for agent in agent_model.schedule.agents if isinstance(agent, ManagerAgent)]
    
    house_agent = house_agents[0] if house_agents else None
    manager_agent = manager_agents[0] if manager_agents else None
    
    print("=== SIMULATION RESULTS FOR HOUSE ===")
    print(f"House ID: {house_agent.unique_id}")
    print(f"Simulation Steps: {simulation_steps}")
    print()
    
    total_recommendations = len([r for r in manager_agent.recommendation_history if r])
    recommendations_given = sum(1 for step_rec in manager_agent.recommendation_history 
                               if step_rec and step_rec.get(house_agent.unique_id) != "maintain")
    recommendation_rate = (recommendations_given / total_recommendations * 100) if total_recommendations > 0 else 0
    
    print("--- RECOMMENDATION STATS ---")
    print(f"Total recommendations given: {recommendations_given}/{total_recommendations}")
    print(f"Recommendation rate: {recommendation_rate:.1f}%")
    
    actions_taken = [house_agent.last_action] + [
        rec.get(house_agent.unique_id, "maintain") for rec in manager_agent.recommendation_history[:-1]
    ]
    increase_actions = actions_taken.count("increase")
    decrease_actions = actions_taken.count("decrease")
    maintain_actions = actions_taken.count("maintain")
    
    print()
    print("--- AGENT ACTIONS ---")
    print(f"Increase actions: {increase_actions}")
    print(f"Decrease actions: {decrease_actions}")
    print(f"Maintain actions: {maintain_actions}")
    
    if house_agent.simulated_consumption:
        original_consumption = sum(house_agent.reference_consumption[i] for i in range(min(simulation_steps, len(house_agent.reference_consumption))))
        simulated_consumption = sum(house_agent.simulated_consumption.values())
        consumption_change = ((simulated_consumption - original_consumption) / original_consumption * 100) if original_consumption > 0 else 0
        
        print()
        print("--- CONSUMPTION IMPACT ---")
        print(f"Original consumption: {original_consumption:.2f} kWh")
        print(f"Simulated consumption: {simulated_consumption:.2f} kWh")
        print(f"Consumption change: {consumption_change:+.2f}%")
    
    if manager_agent.feedback_history:
        compliance_rate = (sum(manager_agent.feedback_history) / len(manager_agent.feedback_history) * 100)
        print()
        print("--- COMPLIANCE ---")
        print(f"Recommendation compliance rate: {compliance_rate:.1f}%")
    
    weekly_avg = sum(house_agent.weekly_consumption.values()) / len(house_agent.weekly_consumption)
    print()
    print("--- BASELINE PROFILE ---")
    print(f"Weekly average consumption: {weekly_avg:.2f} kWh")
    print(f"Total weeks in data: {len(house_agent.weekly_consumption)}")
    
    print("\n=== END SIMULATION RESULTS ===")
