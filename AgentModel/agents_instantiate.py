from AgentModel.house_agent import HouseAgent
from AgentModel.manager_agent import ManagerAgent
from AgentModel.agent_types import AgentType

class InstantiateAgents:
    def __init__(self, agent_model) -> None:
        self.agent_model = agent_model
    
    def instantiate_all_agents(self) -> tuple[list[HouseAgent], ManagerAgent]:
        house_agents: list[HouseAgent] = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
        manager_agents: list[ManagerAgent] = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, ManagerAgent)]

        manager_agent = manager_agents[0] if manager_agents else None
        return house_agents, manager_agent

    def set_agent_type(self, house_agent, agent_type):
        house_agent.agent_type = agent_type

    def set_agents_type(self):
        house_agents = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
        agent_type = AgentType.get_random_type()
        for house_agent in house_agents:
            self.set_agent_type(house_agent, agent_type)