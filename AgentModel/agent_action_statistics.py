class AgentActionStatistics:
    def __init__(self, house_agent, manager_agent, simulation_steps: int) -> None:
        self.house_agent = house_agent
        self.manager_agent = manager_agent
        self.simulation_steps = simulation_steps
    
    def calculate_action_statistics(self):
        actions_taken = [self.house_agent.last_action] + [
            rec.get(self.house_agent.unique_id, "maintain") 
            for rec in self.manager_agent.recommendation_history[:-1]
        ]
        
        increase_actions = actions_taken.count("increase")
        decrease_actions = actions_taken.count("decrease")
        maintain_actions = actions_taken.count("maintain")
        
        return {
            "increase_actions": increase_actions,
            "decrease_actions": decrease_actions,
            "maintain_actions": maintain_actions,
            "total_actions": len(actions_taken)
        }
    
    def print_action_statistics(self):
        stats = self.calculate_action_statistics()
        
        print("--- AGENT ACTIONS ---")
        print(f"Increase actions: {stats['increase_actions']}")
        print(f"Decrease actions: {stats['decrease_actions']}")
        print(f"Maintain actions: {stats['maintain_actions']}")
