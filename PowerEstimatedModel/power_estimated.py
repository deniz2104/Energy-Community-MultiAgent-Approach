from typing import Dict, Optional
from SolarRadiationModel.solar_radiation_house import SolarRadiationHouse

class PowerEstimator(SolarRadiationHouse):
    def __init__(self, house_id: int) -> None:
        super().__init__(house_id)
        self.power_estimated: Dict[str, float] = {}
        self.NEEG: Optional[float] = None
        self.f: float = 0.8
        self.GTSTC: int = 1000
    
    def add_power_estimated(self, timestamp: str, solar_radiatian_value: float, Pmax: int = 575, number_of_panels: int = 1) -> None:
        self.power_estimated[timestamp] = Pmax * self.f * number_of_panels * (solar_radiatian_value / self.GTSTC)

    def determine_NEEG(self) -> None:
        self.NEEG = sum(
            min(self.power_estimated[ts], self.consumption[ts])
            for ts in self.power_estimated
        )