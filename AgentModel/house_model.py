from mesa import Model,time
import random
from .house_agent import HouseAgent
from .manager_agent import ManagerAgent
class HouseModel(Model):
    def __init__(self,n,house_obj,seed=None):
        super().__init__(seed=seed)
        self.num_agents = n
        self.random = random.Random(seed)
        self.step_count=0
        self.schedule = time.RandomActivation(self)
        self.simulation_data = []
        self.create_manager()
        self.create_agents(house_obj)

    def create_agents(self,house_obj):
        for house in house_obj:
            agent = HouseAgent(model=self, unique_id=house.house_id, house_obj=house, agent_type="ideal")
            self.schedule.add(agent)

    def create_manager(self):
        manager_agent = ManagerAgent(unique_id=1,model=self)
        self.schedule.add(manager_agent)

    def step(self):
        manager_agents= [agent for agent in self.schedule.agents if isinstance(agent, ManagerAgent)]
        self.agents.do("step",agents=manager_agents)

        recommendation = manager_agents[0].current_recommendation
        house_agents= [agent for agent in self.schedule.agents if isinstance(agent, HouseAgent)]
        for house in house_agents:
            house.get_recommendation(recommendation)
        self.agents.do("step",agents=house_agents)
        self.step_count += 1
        self.simulation_data.append({
            "step": self.step_count,
            "recommendation": recommendation,
            "followed_recommendation": manager_agents[0].feedback_history[-1]
        })