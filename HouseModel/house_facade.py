from .house_builder import HouseBuilder
from .houses_preprocessing_data import HousesPreprocessingData
from .house_resampling import HouseResampler
from .house_plotter import HousePlotter
from .house_useful_stats import HouseStatistics
from HelperFiles.file_to_handle_absolute_path_imports import *

class HouseFacade:
    def __init__(self):
        self.builder = HouseBuilder()
        self.houses_preprocessor = HousesPreprocessingData()
        self.resampler = HouseResampler()
        self.plotter = HousePlotter()
        self.statistics = HouseStatistics()

    def build_houses(self, csv_path):
        return self.builder.build(csv_path)

    def process_houses_pipeline(self, csv_path, export_path=None):
        houses = self.build_houses(csv_path)
        
        #houses = self.houses_preprocessor.remove_houses_with_few_data_points(houses)
        #print(f"After removing houses with few data points: {len(houses)}")
        
        houses = self.houses_preprocessor.remove_houses_with_lot_of_zeros(houses)

        houses = self.houses_preprocessor.eliminate_houses_with_zero_for_a_period_of_time(houses)

        self.houses_preprocessor.remove_anomalies_in_data(houses)
        
        self.houses_preprocessor.eliminate_days_after_a_year(houses)
        
        houses = self.resampler.resampling_houses_based_on_time_period(houses)

        self.houses_preprocessor.round_remained_high_values(houses)
        
        if export_path:
            self.builder.export_to_csv(houses, export_path)
        
        return houses

    def plot_house_consumption(self, house, month=None, day=None, time_range=None):
        if time_range:
            self.plotter.plot_consumption_over_time_range(house, time_range[0], time_range[1])
        else:
            self.plotter.plot_consumption_over_time(house, month=month, day=day)

    def get_house_statistics(self, house):
        return self.statistics.get_weekly_consumption_by_month(house)