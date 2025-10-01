from mesa import Agent
from AgentModel.house_agent import HouseAgent

class ManagerAgent(Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)

        self.current_recommendation: dict[int, str] = {}
        self.recommendation_history: list[dict[int, str]] = []

    def make_recommendation(self) -> dict[int, str]:
        current_step = self.model.step_count
        current_week = current_step // 168

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

    def step(self) -> None:
        recommendation = self.make_recommendation()
        self.current_recommendation = recommendation
        self.recommendation_history.append(recommendation)
