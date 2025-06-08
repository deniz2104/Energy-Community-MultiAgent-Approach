from mesa import Agent
class HouseAgent(Agent):
    def __init__(self,unique_id,model,house_obj,agent_type="normal"):
        super.__init__(unique_id,model)
        self.base_consumption = house_obj.consumption
        self.agent_type = agent_type
        self.current_consumption=0
        self.current_recommendation = None
        self.followed_recommendation = False
        self.last_action = "maintain"

        self.set_agent_type()
        
    def set_agent_type(self):
        if self.agent_type == "non-enthusiastic":
            self.follow_recommendation=0.3
            self.consume_as_expected= 0.7
        elif self.agent_type == "ideal":
            self.follow_recommendation=1.0
            self.consume_as_expected=0.0
        elif self.agent_type == "enthusiastic":
            self.follow_recommendation=0.7
            self.consume_as_expected=0.3
        else:
            self.follow_recommendation=0.5
            self.consume_as_expected=0.5
        
    def get_recommendation(self,recommendation):
        self.current_recommendation = recommendation
    
    def decide_action(self):
        will_follow_recommendation = self.model.random.random() < self.follow_recommendation
        self.followed_recommendation = will_follow_recommendation

        if not will_follow_recommendation:
            return "maintain"
        
        if self.current_recommendation == "increase":
            return "strongly_increase" if self.agent_type=="enthusiastic" else "moderately_increase"
        elif self.current_recommendation == "decrease":
            return "strongly_decrease" if self.agent_type=="non-enthusiastic" else "moderately_decrease"
        else:
            return "maintain"
        
    def apply_action(self,action,delta_p_moderate=0.2,delta_p_strong=0.2):
        multipliers = {
        "maintain": 1.0,
        "moderately_increase": 1 + delta_p_moderate,
        "strongly_increase": 1 + delta_p_strong,
        "moderately_decrease": 1 - delta_p_moderate,
        "strongly_decrease": 1 - delta_p_strong,
    }
        self.current_consumption = self.base_consumption * multipliers.get(action, 1.0)
    def step(self):
        action=self.decide_action()
        self.last_action = action
        
        self.apply_action(action)