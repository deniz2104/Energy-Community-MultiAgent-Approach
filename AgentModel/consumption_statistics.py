class ConsumptionStatistics:
    def __init__(self, house_agent, simulation_steps: int) -> None:
        self.house_agent = house_agent
        self.simulation_steps = simulation_steps
    
    def calculate_consumption_impact(self):
        if not self.house_agent.simulated_consumption:
            return None
            
        original_consumption = sum(
            self.house_agent.reference_consumption[i] 
            for i in range(min(self.simulation_steps, len(self.house_agent.reference_consumption)))
        )
        simulated_consumption = sum(self.house_agent.simulated_consumption.values())
        
        return {
            "original_consumption": original_consumption,
            "simulated_consumption": simulated_consumption,
        }
    
    def calculate_consumption_differences(self):
        if not self.house_agent.simulated_consumption:
            return None
        
        cumulative_differences = 0
        for i in range(min(self.simulation_steps,len(self.house_agent.reference_consumption))):
            original = self.house_agent.reference_consumption.get(i)
            simulated = self.house_agent.simulated_consumption.get(i, original)
            cumulative_differences += simulated - original
        return cumulative_differences / self.simulation_steps

    def calculate_baseline_profile(self):
        weekly_avg = sum(self.house_agent.weekly_consumption.values()) / len(self.house_agent.weekly_consumption)
        total_weeks = len(self.house_agent.weekly_consumption)
        
        return {
            "weekly_average_consumption": weekly_avg,
            "total_weeks_in_data": total_weeks
        }
    
    def print_consumption_statistics(self):
        impact_stats = self.calculate_consumption_impact()
        baseline_stats = self.calculate_baseline_profile()
        percentage_change = self.calculate_consumption_differences()

        if impact_stats:
            print("--- CONSUMPTION IMPACT ---")
            print(f"Original consumption: {impact_stats['original_consumption']:.2f} kWh")
            print(f"Simulated consumption: {impact_stats['simulated_consumption']:.2f} kWh")
            print()
        
        print("--- BASELINE PROFILE ---")
        print(f"Weekly average consumption: {baseline_stats['weekly_average_consumption']:.2f} kWh")
        print(f"Total weeks in data: {baseline_stats['total_weeks_in_data']}")
        print()

        print("--- PERCENTAGE CHANGE ---")
        print(f"Percentage change in consumption: {percentage_change:.2f}%")
