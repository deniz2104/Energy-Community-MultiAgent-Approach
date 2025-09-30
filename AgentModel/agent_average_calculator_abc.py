from abc import ABC
from AgentModel.house_agent import HouseAgent

class AgentAverageCalculatorABC(ABC):

    def __init__(self, agent_model):
        self.agent_model = agent_model
    
    def calculate_average(self, attribute_name: str) -> float:
        house_agents = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
        if not house_agents:
            return 0.0
            
        total_value = 0.0
        for house_agent in house_agents:
            total_value += getattr(house_agent, attribute_name, 0.0)

        return total_value / len(house_agents)
