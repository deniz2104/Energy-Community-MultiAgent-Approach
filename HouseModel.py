from mesa import Model
import random
from HouseAgent import HouseAgent
from ManagerAgent import ManagerAgent
class HouseModel(Model):
    def __init__(self,n,house_id,house_obj,agent_type="normal",seed=None):
        super().__init__(seed=seed)
        self.num_agents = n
        self.random = random.Random(seed)
        self.house_agent = HouseAgent(model=self,unique_id=house_id,house_obj=house_obj,agent_type=agent_type)
        self.manager_agent = ManagerAgent(model=self,unique_id=1,house_obj=house_obj)
        self.step_count=0
        self.simulation_data = []

    def step(self):
        self.manager_agent.step()
        recommendation = self.manager_agent.recommendation