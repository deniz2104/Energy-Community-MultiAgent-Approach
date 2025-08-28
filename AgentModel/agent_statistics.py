from AgentModel.house_agent import HouseAgent
from AgentModel.agents_instantiate import InstantiateAgents
from AgentModel.manager_agent import ManagerAgent
from AgentModel.agent_run_model import RunModel
from AgentModel.agent_action_statistics import AgentActionStatistics
from AgentModel.agent_consumption_statistics import ConsumptionStatistics
from AgentModel.agent_recommendation_statistics import RecommendationStatistics

class AgentStatistics:
    def __init__(self, agent_model, simulation_steps: int) -> None:
        self.agent_model = agent_model
        self.simulation_steps = simulation_steps
        self.instantiate_agents = InstantiateAgents(agent_model)
        self.run_model = RunModel(agent_model, simulation_steps)
        
        self.action_statistics: list[AgentActionStatistics] = []
        self.consumption_statistics: list[ConsumptionStatistics] = []
        self.recommendation_statistics: list[RecommendationStatistics] = []

    def run_simulation_and_generate_statistics(self) -> tuple[list[HouseAgent], ManagerAgent]:
        house_agents, manager_agent = self.instantiate_agents.instantiate_all_agents()

        self.run_model.run()

        self.action_statistics = []
        self.consumption_statistics = []
        self.recommendation_statistics = []
        
        for house_agent in house_agents:
            self.action_statistics.append(AgentActionStatistics(house_agent, manager_agent, self.simulation_steps))
            self.consumption_statistics.append(ConsumptionStatistics(house_agent, self.simulation_steps))
            self.recommendation_statistics.append(RecommendationStatistics(house_agent, manager_agent, self.simulation_steps))
        
        return house_agents, manager_agent

    def print_all_statistics(self) -> None:
        if not self.action_statistics or not self.consumption_statistics or not self.recommendation_statistics:
            print("Simulation not run yet. Please run the simulation first.")
            return

        print("=" * 60)
        print("STATISTICS FOR ALL HOUSE AGENTS")
        print("=" * 60)
        
        for agent_index, (rec_stats, action_stats, cons_stats) in enumerate(zip(
            self.recommendation_statistics, 
            self.action_statistics, 
            self.consumption_statistics
        )):
            print(f"\n--- HOUSE AGENT {agent_index + 1} (ID: {action_stats.house_agent.unique_id}) ---")
            print("-" * 40)
            
            rec_stats.print_recommendation_statistics()
            print()
            action_stats.print_action_statistics()
            print()
            cons_stats.print_consumption_statistics()
            
            if agent_index < len(self.action_statistics) - 1:
                print("\n" + "=" * 60)
