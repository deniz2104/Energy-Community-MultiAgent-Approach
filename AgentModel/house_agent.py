from mesa import Agent
from statistics import mean
from typing import Optional

class HouseAgent(Agent):
    def __init__(self,unique_id : int,model,house_obj,agent_type="ideal",recommendation_dictionary : Optional[dict[int,int]]= None) -> None:
        super().__init__(unique_id,model)

        common_timestamps : list[int] = self.define_common_timestamps(house_obj)

        self.base_consumption = {
            i: house_obj.power_estimated[common_timestamps[i]]
            for i in range(len(common_timestamps))
        }

        self.reference_consumption = {
            i: house_obj.consumption[common_timestamps[i]]
            for i in range(len(common_timestamps))
        }

        self.weekly_consumption : dict[int,float] = self.define_weekly_consumption()
        self.agent_type : str = agent_type
        self.simulated_consumption : dict[int,float] = {}
        self.current_recommendation = "maintain"
        self.followed_recommendation : bool = False
        self.self_consumption :float = house_obj.self_consumption
        self.self_sufficiency : float = house_obj.self_sufficiency
        self.simulated_self_consumption : float = 0.0
        self.simulated_self_sufficiency : float = 0.0
        self.last_action = "maintain"

        self.recommendation_dictionary = recommendation_dictionary if recommendation_dictionary is not None else {}

        self.set_agent_type()

    def define_weekly_consumption(self) -> dict[int,float]:
        weekly_consumption = {}
        for i in range(len(self.base_consumption)//168):
            weekly_consumption[i] = mean(list(self.base_consumption.values())[i*168:(i+1)*168])
        if((len(self.base_consumption)-len(weekly_consumption)*168) % 168!= 0):
            weekly_consumption[len(weekly_consumption)] = mean(list(self.base_consumption.values())[-(len(self.base_consumption)-len(weekly_consumption)*168):])
        return weekly_consumption

    def define_common_timestamps(self, house_obj) -> list[int]:
        consumption_timestamps = set(house_obj.consumption.keys())
        power_estimated_timestamps = set(house_obj.power_estimated.keys())
        common_timestamps = sorted(consumption_timestamps.intersection(power_estimated_timestamps))
        return common_timestamps

    def set_agent_type(self) -> None:
        if self.agent_type == "ideal":
            self.follow_recommendation = 1.0
        elif self.agent_type == "enthusiastic":
            self.follow_recommendation = 0.7
        elif self.agent_type == "non-enthusiastic":
            self.follow_recommendation = 0.3   

    def get_recommendation(self,recommendation) -> None: 
        self.current_recommendation = recommendation if recommendation else "maintain"

    def decide_action(self) -> Optional[str]:
        will_follow_recommendation = self.model.random.random() < self.follow_recommendation
        self.followed_recommendation = will_follow_recommendation

        if not will_follow_recommendation:
            return "maintain"
        
        return self.current_recommendation

    def apply_action(self,action,delta_p=0.2) -> None:
        multipliers = {
        "maintain": 1.0,
        "increase": 1 + delta_p,
        "decrease": 1 - delta_p,
    }
        self.simulated_consumption[self.model.step_count] = self.reference_consumption[self.model.step_count] * multipliers.get(action, 1.0)

    def determine_simulated_self_consumption_and_self_sufficiency(self) -> None:
        denominator_for_self_consumption = 0.0
        numerator_for_self_consumption = 0.0
        denominator_for_self_sufficiency = 0.0
        numerator_for_self_sufficiency = 0.0

        for step, simulated_consumption in self.simulated_consumption.items():
            base_prod = self.base_consumption[step]
            min_value = min(simulated_consumption, base_prod)

            denominator_for_self_consumption += simulated_consumption
            numerator_for_self_consumption += min_value
                
            denominator_for_self_sufficiency += base_prod
            numerator_for_self_sufficiency += min_value

        self.simulated_self_consumption = numerator_for_self_consumption / denominator_for_self_consumption if denominator_for_self_consumption > 0 else 0
        self.simulated_self_sufficiency = numerator_for_self_sufficiency / denominator_for_self_sufficiency if denominator_for_self_sufficiency > 0 else 0

    def step(self) -> None:
        action=self.decide_action()
        self.last_action = action
        
        self.apply_action(action)
        self.determine_simulated_self_consumption_and_self_sufficiency()