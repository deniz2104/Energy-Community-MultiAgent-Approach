from typing import Optional
from mesa import Model,time
import random
from AgentModel.house_agent import HouseAgent
from AgentModel.manager_agent import ManagerAgent

class HouseModel(Model):
    def __init__(self,n,house_obj,recommendation_dictionaries: Optional[dict[int,int]]=None,seed: Optional[int]=None)-> None:
        super().__init__(seed=seed)
        self.num_agents = n
        self.random = random.Random(seed)
        self.step_count=0
        self.schedule = time.RandomActivation(self)
        self.recommendation_dictionaries = recommendation_dictionaries if recommendation_dictionaries is not None else {}
        self.create_manager()
        self.create_agents(house_obj)

    def create_agents(self,house_obj)-> None:
        for house in house_obj:
            house_recommendation_dict = self.recommendation_dictionaries.get(house.house_id, {})
            
            if isinstance(house_recommendation_dict, dict):
                recommendation_dict = house_recommendation_dict
            else:
                recommendation_dict = {}
            
            agent = HouseAgent(
                unique_id=house.house_id,
                model=self, 
                house_obj=house, 
                agent_type="ideal",
                recommendation_dictionary=recommendation_dict
            )
            self.schedule.add(agent)

    def create_manager(self)-> None:
        manager_agent = ManagerAgent(unique_id=1,model=self)
        self.schedule.add(manager_agent)

    def step(self) -> None:
        manager_agents= [agent for agent in self.schedule.agents if isinstance(agent, ManagerAgent)]
        for manager in manager_agents:
            manager.step()

        recommendations :dict[int,str]= manager_agents[0].current_recommendation
        house_agents= [agent for agent in self.schedule.agents if isinstance(agent, HouseAgent)]
        for house in house_agents:
            house_recommendation = recommendations.get(house.unique_id, "maintain")
            house.get_recommendation(house_recommendation)
            
        for house in house_agents:
            house.step()
            
        self.step_count += 1