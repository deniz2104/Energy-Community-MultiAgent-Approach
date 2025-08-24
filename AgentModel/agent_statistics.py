from logging import Manager
from AgentModel.house_agent import HouseAgent
from AgentModel.instantiate_agents import InstantiateAgents
from AgentModel.manager_agent import ManagerAgent
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

    def run_simulation_and_generate_statistics(self) -> tuple[HouseAgent, ManagerAgent]:
        house_agent, manager_agent = self.instantiate_agents.instantiate_agents()
        
        self.run_model.run()

        self.action_statistics = AgentActionStatistics(house_agent, manager_agent, self.simulation_steps)
        self.consumption_statistics = ConsumptionStatistics(house_agent, self.simulation_steps)
        self.recommendation_statistics = RecommendationStatistics(house_agent, manager_agent, self.simulation_steps)
        
        return house_agent, manager_agent
    
    def print_all_statistics(self) -> None:
        if self.action_statistics is None or self.consumption_statistics is None or self.recommendation_statistics is None:
            print("Simulation not run yet. Please run the simulation first.")
            return

        self.recommendation_statistics.print_recommendation_statistics()
        print()
        self.action_statistics.print_action_statistics()
        print()
        self.consumption_statistics.print_consumption_statistics()
    
    def get_all_statistics(self) -> dict[str, float | None]:
        if not all([self.action_statistics, self.consumption_statistics, self.recommendation_statistics]):
            return {}
            
        stats = {}
        
        recommendation_stats = self.recommendation_statistics.calculate_recommendation_statistics() if self.recommendation_statistics else None
        stats.update(recommendation_stats if recommendation_stats else {})
        
        action_stats = self.action_statistics.calculate_action_statistics() if self.action_statistics else None
        stats.update(action_stats if action_stats else {})
        
        consumption_impact = self.consumption_statistics.calculate_consumption_impact() if self.consumption_statistics else None
        stats.update(consumption_impact if consumption_impact else {})
        
        baseline_profile = self.consumption_statistics.calculate_baseline_profile() if self.consumption_statistics else None
        stats.update(baseline_profile if baseline_profile else {})

        return stats
