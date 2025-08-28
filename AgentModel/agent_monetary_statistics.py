from AgentModel.house_agent import HouseAgent
from typing import Final

class AgentMonetaryStatistics:
    def __init__(self, agent_model, simulation_steps):
        self.agent_model = agent_model
        self.house_agents = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
        self.price_per_kwh: Final[float] = 1.31
        self.simulation_steps = simulation_steps

    def calculate_total_estimated_consumption(self):
        sum_of_consumption = 0.0
        for agent in self.house_agents:
            sum_of_consumption += sum(agent.reference_consumption[i] for i in range(min(self.simulation_steps, len(agent.reference_consumption))))
        return sum_of_consumption / 1000.0  

    def calculate_total_simulated_consumption(self):
        sum_of_consumption = 0.0
        for agent in self.house_agents:
            sum_of_consumption += sum(agent.simulated_consumption.values())
        return sum_of_consumption / 1000.0  
    
    def simulated_savings(self):
        total_estimated = self.calculate_total_estimated_consumption()
        total_simulated = self.calculate_total_simulated_consumption()
        savings = (total_estimated - total_simulated) * self.price_per_kwh
        return savings
