class House():
    def __init__(self, house_id: int) -> None:
        self.house_id: int = house_id
        self.consumption: dict[str, float] = {}
        
    def add_consumption(self, timestamp: str, consumption_value: float) -> None:
        self.consumption[timestamp] = consumption_value