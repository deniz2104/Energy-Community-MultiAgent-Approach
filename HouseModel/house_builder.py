import csv
from .house import House

class HouseBuilder():
    def __init__(self) -> None:
        pass
        
    def open_csv_file(self, csv_path: str) -> list[tuple[int, str, float]]:
        results: list[tuple[int, str, float]] = []
        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                timestamp = row['EpochTime']
                consumption = float(row['TotalConsumption'])
                results.append((house_id, timestamp, consumption))
        return results
        
    def build(self, csv_path: str) -> list[House]:
        houses: dict[int, House] = {}
        rows = self.open_csv_file(csv_path)
        for house_id, timestamp, consumption in rows:
            if house_id not in houses:
                houses[house_id] = House(house_id)

            houses[house_id].add_consumption(timestamp, consumption)

        return list(houses.values())

    def export_to_csv(self, houses: list[House], file_path: str) -> None:
         with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalConsumption'])
            for house in houses:
                for timestamp, consumption in house.consumption.items():
                    writer.writerow([house.house_id, timestamp, consumption])
