from mesa import Agent

class ManagerAgent(Agent):
    def __init__(self,unique_id,model):
        super.__init__(unique_id,model)

        self.current_recomandation = None
        self.recommendation_history = []
        self.feedback_history = []

    def make_recommendation(self):
        pass

    def receive_feedback(self,follow_recommendation):
        self.feedback_history.append(1 if follow_recommendation else 0)
    
    def step(self):
        recommendation = self.make_recommendation()
        self.current_recomandation=recommendation
        self.recommendation_history.append(recommendation)

        if self.model.step_count > 0:
            last_feedback = self.model.simulation_data[-1]["followed_recommendation"]
            self.receive_feedback(last_feedback)
