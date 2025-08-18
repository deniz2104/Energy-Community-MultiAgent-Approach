from mesa import Agent
from statistics import mean

class HouseAgent(Agent):
    def __init__(self,unique_id,model,house_obj,agent_type="ideal",recommendation_dictionary=None):
        super().__init__(unique_id,model)
        
        common_timestamps = self.define_common_timestamps(house_obj)

        self.base_consumption = {
            i: house_obj.power_estimated[common_timestamps[i]]
            for i in range(len(common_timestamps))
        }

        self.reference_consumption = {
            i: house_obj.consumption[common_timestamps[i]]
            for i in range(len(common_timestamps))
        }

        self.weekly_consumption = self.define_weekly_consumption()
        self.agent_type = agent_type
        self.simulated_consumption = {}
        self.current_recommendation = None
        self.followed_recommendation = False
        self.last_action = "maintain"

        self.recommendation_dictionary = recommendation_dictionary if recommendation_dictionary is not None else {}

        self.set_agent_type()

    def define_weekly_consumption(self):
        weekly_consumption = {}
        for i in range(len(self.base_consumption)//168):
            weekly_consumption[i] = mean(list(self.base_consumption.values())[i*168:(i+1)*168])
        if((len(self.base_consumption)-len(weekly_consumption)*168) % 168!= 0):
               weekly_consumption[len(weekly_consumption)] = mean(list(self.base_consumption.values())[-(len(self.base_consumption)-len(weekly_consumption)*168):])
        return weekly_consumption

    def define_common_timestamps(self, house_obj):
        consumption_timestamps = set(house_obj.consumption.keys())
        power_estimated_timestamps = set(house_obj.power_estimated.keys())
        common_timestamps = sorted(consumption_timestamps.intersection(power_estimated_timestamps))
        return common_timestamps

    def set_agent_type(self):
        self.follow_recommendation=1.0
        self.consume_as_expected=0.0
        
    def get_recommendation(self,recommendation):
        self.current_recommendation = recommendation
    
    def decide_action(self):
        will_follow_recommendation = self.model.random.random() < self.follow_recommendation
        self.followed_recommendation = will_follow_recommendation

        if not will_follow_recommendation:
            return "maintain"
        
        return self.current_recommendation
        
    def apply_action(self,action,delta_p=0.2):
        multipliers = {
        "maintain": 1.0,
        "increase": 1 + delta_p,
        "decrease": 1 - delta_p,
    }
        self.simulated_consumption[self.model.step_count] = self.reference_consumption[self.model.step_count] * multipliers.get(action, 1.0)

    def step(self):
        action=self.decide_action()
        self.last_action = action
        
        self.apply_action(action)