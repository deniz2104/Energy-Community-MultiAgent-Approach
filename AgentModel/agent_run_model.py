class RunModel:
    def __init__(self, agent_model, simulation_steps: int) -> None:
        self.agent_model = agent_model
        self.simulation_steps = simulation_steps

    def run(self) -> None:
        for _ in range(self.simulation_steps):
            self.agent_model.step()