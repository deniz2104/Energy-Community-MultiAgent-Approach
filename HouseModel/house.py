from CsvModel.csv_core import open_csv_file

class House():
    _instances: dict[int, "House"] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._instances = {}

    def __init__(self, house_id: int) -> None:
        self.house_id: int = house_id
        self.consumption: dict[str, float] = {}
        type(self)._instances[house_id] = self

    @classmethod
    def get_or_create(cls, house_id: int) -> "House":
        if house_id not in cls._instances:
            cls(house_id)
        return cls._instances[house_id]

    @classmethod
    def unregister(cls, house_id: int) -> None:
        cls._instances.pop(house_id, None)

    @classmethod
    def reset(cls) -> None:
        cls._instances.clear()

    @classmethod
    def build(cls, csv_path: str) -> list["House"]:
        cls.reset()
        for house_id, timestamp, consumption in open_csv_file(csv_path):
            cls.get_or_create(house_id).add_consumption(timestamp, consumption)
        return cls.get_instances()

    @classmethod
    def get_instances(cls) -> list["House"]:
        return list(cls._instances.values())

    @classmethod
    def count_instances(cls) -> int:
        return len(cls._instances)

    @classmethod
    def return_ids_of_instances(cls) -> list[int]:
        return list(cls._instances.keys())

    @classmethod 
    def houses_data_to_rows(cls) -> list[tuple[int, str, float]]:
        return [(house.house_id, timestamp, consumption) for house in cls._instances.values() for timestamp, consumption in zip(house.timestamps, house.consumption_values)]

    def add_consumption(self, timestamp: str, consumption_value: float) -> None:
        self.consumption[timestamp] = consumption_value

    @property
    def timestamps(self) -> list[str]:
        return list(self.consumption.keys())

    @property
    def consumption_values(self) -> list[float]:
        return list(self.consumption.values())
