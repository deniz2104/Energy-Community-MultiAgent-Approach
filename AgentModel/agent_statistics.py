from AgentModel.instantiate_agents import InstantiateAgents
from AgentModel.run_model import RunModel
from AgentModel.agent_action_statistics import AgentActionStatistics
from AgentModel.consumption_statistics import ConsumptionStatistics
from AgentModel.recommendation_statistics import RecommendationStatistics

class AgentStatistics:
    def __init__(self, agent_model, simulation_steps: int) -> None:
        self.agent_model = agent_model
        self.simulation_steps = simulation_steps
        self.instantiate_agents = InstantiateAgents(agent_model)
        self.run_model = RunModel(agent_model, simulation_steps)
        
        self.action_statistics = None
        self.consumption_statistics = None
        self.recommendation_statistics = None
    
    def run_simulation_and_generate_statistics(self):
        house_agent, manager_agent = self.instantiate_agents.instantiate_agents()
        
        self.run_model.run()

        self.action_statistics = AgentActionStatistics(house_agent, manager_agent, self.simulation_steps)
        self.consumption_statistics = ConsumptionStatistics(house_agent, self.simulation_steps)
        self.recommendation_statistics = RecommendationStatistics(house_agent, manager_agent, self.simulation_steps)
        
        return house_agent, manager_agent
    
    def print_all_statistics(self):
        if not all([self.action_statistics, self.consumption_statistics, self.recommendation_statistics]):
            print("Statistics not initialized. Run simulation first.")
            return
            
        self.recommendation_statistics.print_recommendation_statistics()
        print()
        self.action_statistics.print_action_statistics()
        print()
        self.consumption_statistics.print_consumption_statistics()
    
    def get_all_statistics(self):
        if not all([self.action_statistics, self.consumption_statistics, self.recommendation_statistics]):
            return None
            
        stats = {}
        stats.update(self.recommendation_statistics.calculate_recommendation_statistics())
        stats.update(self.action_statistics.calculate_action_statistics())
        
        consumption_impact = self.consumption_statistics.calculate_consumption_impact()
        if consumption_impact:
            stats.update(consumption_impact)
            
        baseline_profile = self.consumption_statistics.calculate_baseline_profile()
        stats.update(baseline_profile)
        
        return stats 
