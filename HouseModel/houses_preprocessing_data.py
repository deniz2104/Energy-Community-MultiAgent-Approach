from .house_preprocessing_data import HousePreprocessingData
class HousesPreprocessingData:
    def __init__(self):
        self.house_preprocessing = HousePreprocessingData()

    def remove_houses_with_few_data_points(self, houses):
        houses_with_enough_data = [house for house in houses if len(house.consumption) >= 50000]
        return list(houses_with_enough_data)
    
    def remove_houses_with_lot_of_zeros(self,houses):
        houses_to_consider=[house for house in houses if self.house_preprocessing.count_zero_for_house(house) < 0.15*len(house.consumption)]
        return list(houses_to_consider)
    
    def remove_anomalies_in_data(self, houses):
        for house in houses:
            self.house_preprocessing.eliminate_anomalies_in_data(house)
    def eliminate_days_after_a_year(self, houses):
        for house in houses:
            self.house_preprocessing.eliminate_days_after_a_year_per_house(house)
    def eliminate_houses_with_zero_for_a_period_of_time(self, houses):
        houses_with_no_eliminated_houses = [house for house in houses if self.house_preprocessing.remove_houses_having_zero_for_a_period_of_time(house)==0]
        return list(houses_with_no_eliminated_houses)
    
    def round_remained_high_values(self, houses):
        for house in houses:
            self.house_preprocessing.round_remained_anomalies(house)