from abc import ABC
from AgentModel.house_agent import HouseAgent

class AgentAverageCalculatorABC(ABC):

    def __init__(self, agent_model):
        self.agent_model = agent_model
        self.house_agents = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
    
    def calculate_average(self, attribute_name: str) -> float:
        if not self.house_agents:
            return 0.0
            
        total_value = 0.0
        for house_agent in self.house_agents:
            total_value += getattr(house_agent, attribute_name, 0.0)
        
        return total_value / len(self.house_agents)
