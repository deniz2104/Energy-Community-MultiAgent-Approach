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
        if self.agent_type == "non-ethusiastic":
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
        
        if self.current_recommendation is "increase":
            if self.agent_type=="enthusiastic":
                return "strongly_increase"
            else:
                return "moderately_increase"
        elif self.current_recommendation is "decrease":
            if self.agent_type=="non-ethusiastic":
                return "strongly_decrease"
            else:
                return "moderately_decrease"
        else:
            return "maintain"
        
    def apply_action(self,action,delta_p_moderate,delta_p_strong):
        if action=="maintain":
            self.current_consumption=self.base_consumption
        elif action=="moderately_increase":
            self.current_consumption=(1+delta_p_moderate)*self.base_consumption
        elif action=="strongly_increase":
            self.current_consumption=(1+delta_p_strong)*self.base_consumption
        elif action=="moderately_decrease":
            self.current_consumption=(1-delta_p_moderate)*self.base_consumption
        elif action=="strongly_decrease":
            self.current_consumption=(1-delta_p_strong)*self.base_consumption
    def step(self):
        action=self.decide_action()
        self.last_action = action
        
        self.apply_action(action)