from mesa import Agent

class ManagerAgent(Agent):

## ca sa vizualizez rezultatele, reprezentam consumul estimat in timp, productia estimata in timp, consumul simulat in timp (pe acelasi grafic),un calcul de autoconsum simulat/estimat, la fel si autonomie si recomandarile pe un grafic separat(bar chart)
    
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)

        self.current_recommendation = None
        self.recommendation_history = []
        self.feedback_history = []

    def make_recommendation(self):
        current_step=self.model.step_count
        current_week= current_step // 168

        from AgentModel.house_agent import HouseAgent
        houses = [agent for agent in self.model.schedule.agents if isinstance(agent, HouseAgent)]
        recommendations = {}
        
        for house in houses:
            current_consumption = house.reference_consumption[current_step]
            weekly_avg = house.weekly_consumption[current_week]

            if house.recommendation_dictionary.get(current_step,0)==1:
                if current_consumption > 1.1 * weekly_avg:
                    recommendation = "increase"
                elif current_consumption < 0.9 * weekly_avg:
                    recommendation = "decrease"
                else:
                    recommendation = "maintain"
            else:
                recommendation = "maintain"
            
            house.current_recommendation = recommendation
            recommendations[house.unique_id] = recommendation
        
        return recommendations

    def receive_feedback(self,follow_recommendation):
        self.feedback_history.append(1 if follow_recommendation else 0)
    
    def step(self):
        self.current_recommendation=self.make_recommendation()
        self.recommendation_history.append(self.current_recommendation)

        if len(self.model.simulation_data) > 0:
            last_feedback = self.model.simulation_data[-1]["followed_recommendation"]
            self.receive_feedback(last_feedback)