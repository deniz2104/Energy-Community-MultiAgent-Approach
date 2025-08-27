from AgentModel.agent_average_calculator_abc import AgentAverageCalculatorABC


class AgentsSelfSufficiencySelfConsumption(AgentAverageCalculatorABC):
    def determine_estimated_self_sufficiency(self):
        return self.calculate_average('self_sufficiency')

    def determine_estimated_self_consumption(self):
        return self.calculate_average('self_consumption')

    def determine_simulated_self_sufficiency(self):
        return self.calculate_average('simulated_self_sufficiency')

    def determine_simulated_self_consumption(self):
        return self.calculate_average('simulated_self_consumption')
