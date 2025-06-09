from mesa import Agent
from HouseAgent import HouseAgent
class ManagerAgent(Agent):
    def __init__(self,unique_id,model):
        super.__init__(unique_id,model)

        self.current_recommendation = None
        self.recommendation_history = []
        self.feedback_history = []

    def make_recommendation(self):
        current_step=self.model.step_count
        current_week= current_step // 168

        houses = [agent for agent in self.model.schedule.agents if isinstance(agent, HouseAgent)]
        for house in houses:
            current_consumption = house.base_consumption[current_step]
            weekly_avg = house.weekly_consumption[current_week]

            if current_consumption >1.1*weekly_avg:
                house.current_recommendation = "increase"
            elif current_consumption <0.9*weekly_avg:
                house.current_recommendation = "decrease"
            else:
                house.current_recommendation = "maintain"

    def receive_feedback(self,follow_recommendation):
        self.feedback_history.append(1 if follow_recommendation else 0)
    
    def step(self):
        recommendation = self.make_recommendation()
        self.current_recommendation=recommendation
        self.recommendation_history.append(recommendation)

        if self.model.step_count > 0:
            last_feedback = self.model.simulation_data[-1]["followed_recommendation"]
            self.receive_feedback(last_feedback)
