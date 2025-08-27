class RecommendationStatistics:
    def __init__(self, house_agent, manager_agent, simulation_steps: int) -> None:
        self.house_agent = house_agent
        self.manager_agent = manager_agent
        self.simulation_steps = simulation_steps

    def calculate_recommendation_statistics(self) -> dict[str, float | None]:
        total_recommendations = len([r for r in self.manager_agent.recommendation_history if r])
        recommendations_given = sum(
            1 for step_rec in self.manager_agent.recommendation_history 
            if step_rec and step_rec.get(self.house_agent.unique_id) != "maintain"
        )
        recommendation_rate = (
            (recommendations_given / total_recommendations * 100) 
            if total_recommendations > 0 else 0
        )
        
        return {
            "total_recommendations": total_recommendations,
            "recommendations_given": recommendations_given,
            "recommendation_rate": recommendation_rate
        }

    def print_recommendation_statistics(self) -> None:
        stats = self.calculate_recommendation_statistics()
        
        print("--- RECOMMENDATION STATS ---")
        print(f"Total recommendations given: {stats['recommendations_given']}/{stats['total_recommendations']}")
        print(f"Recommendation rate: {stats['recommendation_rate']:.1f}%")
