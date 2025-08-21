from AgentModel.house_agent import HouseAgent
from AgentModel.manager_agent import ManagerAgent

class InstantiateAgents:
    def __init__(self, agent_model) -> None:
        self.agent_model = agent_model

    def instantiate_agents(self) -> tuple[HouseAgent, ManagerAgent]:
        house_agents: list[HouseAgent] = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
        manager_agents: list[ManagerAgent] = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, ManagerAgent)]

        house_agent = house_agents[0] if house_agents else None
        manager_agent = manager_agents[0] if manager_agents else None
        return house_agent, manager_agent