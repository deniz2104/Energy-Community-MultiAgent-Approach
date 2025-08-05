from typing import Optional
from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id: int) -> None:
        super().__init__(house_id)
        self.power_estimated: dict[str, float] = {}
        self.NEEG: Optional[float] = None
        self.f: float = 0.8
        self.GTSTC: int = 1000
        self.number_of_panels: int = 10

    def add_power_estimated(self, timestamp: str, solar_radiation_value: float, Pmax: int = 575) -> None:
        self.power_estimated[timestamp] = Pmax * self.f * self.number_of_panels * (solar_radiation_value / self.GTSTC)

    def determine_NEEG(self) -> None:
        self.NEEG = sum(
            min(self.power_estimated[ts], self.consumption[ts])
            for ts in self.power_estimated
        )