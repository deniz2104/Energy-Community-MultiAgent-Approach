from CsvModel.csv_core import open_csv_file

class SolarRadiationHouse():
    _instances: dict[int, "SolarRadiationHouse"] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._instances = {}

    def __init__(self, house_id: int) -> None:
        self.house_id: int = house_id
        self.solar_radiation: dict[str, float] = {}
        type(self)._instances[house_id] = self

    @classmethod
    def get_or_create(cls, house_id: int) -> "SolarRadiationHouse":
        if house_id not in cls._instances:
            cls(house_id)
        return cls._instances[house_id]

    @classmethod
    def get_instances(cls) -> list["SolarRadiationHouse"]:
        return list(cls._instances.values())
    
    @classmethod
    def reset(cls) -> None:
        cls._instances.clear()

    @classmethod
    def return_ids_of_instances(cls) -> list[int]:
        return list(cls._instances.keys()) 

    @classmethod
    def build(cls, csv_path: str) -> list["SolarRadiationHouse"]:
        cls.reset()
        for house_id, timestamp, consumption in open_csv_file(csv_path):
            cls.get_or_create(house_id).add_solar_radiation(timestamp, consumption)
        return cls.get_instances()

    def add_solar_radiation(self, timestamp: str, solar_radiation_data: float) -> None:
        self.solar_radiation[timestamp] = solar_radiation_data