from AgentModel.house_agent import HouseAgent
import sys

class AgentSimulationSteps():
    def __init__(self,agent_model):
        self.agent_model = agent_model

    def get_maximum_simulation_steps(self,houses):
        house_agents: list[HouseAgent] = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]
        simulation_steps = sys.maxsize
        for index_agent in range(self.agent_model.num_agents):
            simulation_steps = min(simulation_steps, len(house_agents[index_agent].define_common_timestamps(houses[index_agent])))

        return simulation_steps
