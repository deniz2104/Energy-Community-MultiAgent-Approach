import csv
from house import House
from collections import OrderedDict

class HouseBuilder():
    def __init__(self):
        pass
    def open_csv_file(self, csv_path):
        results=[]
        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                timestamp = row['EpochTime']
                value = float(row['TotalValue'])
                results.append((house_id, timestamp, value))
        return results
    def build(self, csv_path):
        houses = {}
        rows= self.open_csv_file(csv_path)
        for house_id, timestamp, value in rows:
            if house_id not in houses:
                houses[house_id] = House(house_id)

            houses[house_id].add_consumption(timestamp, value)

        return list(houses.values())

    def resampling_houses_based_on_time_period(self, houses):
        resampled_houses={}
        for house in houses:
            timestamps, consumption = house.prepare_house_for_resampling()
            resampled_house = House(house.house_id)
            resampled_houses[house.house_id] = resampled_house

            for ts, cons in zip(timestamps, consumption):
                resampled_house.add_consumption(ts, cons)

            sorted_consumption = sorted(resampled_house.consumption.items(), key=lambda x: x[0])
            resampled_house.consumption = OrderedDict(sorted_consumption)
        return list(resampled_houses.values())

    
    def remove_houses_with_few_data_points(self, houses):
        houses_with_enough_data = [house for house in houses if len(house.consumption) >= 50000]
        return list(houses_with_enough_data)
    def remove_houses_with_lot_of_zeros(self,houses):
        houses_to_consider=[house for house in houses if house.count_zero_for_house() < 0.15*len(house.consumption)]
        return list(houses_to_consider)
    def remove_anomalies_in_data(self, houses):
        for house in houses:
            house.eliminate_anomalies_in_data()
    def eliminate_days_after_a_year(self, houses):
        for house in houses:
            house.eliminate_days_after_a_year_per_house()
    def eliminate_houses_with_zero_for_a_period_of_time(self, houses):
        houses_with_no_eliminated_houses = [house for house in houses if house.remove_houses_having_zero_for_a_period_of_time()==0]
        return list(houses_with_no_eliminated_houses)