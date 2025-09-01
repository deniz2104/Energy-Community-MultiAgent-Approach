from typing import Optional
from HouseModel.house_builder import HouseBuilder
from HouseModel.houses_preprocessing_data import HousesPreprocessingData
from HouseModel.house_resampling import HouseResampler
from HouseModel.house_plotter import HousePlotter
from HouseModel.house import House

class HouseFacade:
    def __init__(self) -> None:
        self.builder = HouseBuilder()
        self.houses_preprocessor = HousesPreprocessingData()
        self.resampler = HouseResampler()
        self.plotter = HousePlotter()

    def build_houses(self, csv_path: str) -> list[House]:
        return self.builder.build(csv_path)

    def process_houses_pipeline(self, csv_path: str, export_path: Optional[str] = None) -> list[House]:
        houses = self.build_houses(csv_path)
        
        houses = self.houses_preprocessor.remove_houses_with_few_data_points(houses)
        
        houses = self.houses_preprocessor.remove_houses_with_lot_of_zeros(houses)

        houses = self.houses_preprocessor.eliminate_houses_with_zero_for_a_period_of_time(houses)

        self.houses_preprocessor.remove_anomalies_in_data(houses)
        
        self.houses_preprocessor.eliminate_days_after_a_year(houses)
        
        houses = self.resampler.resampling_houses_based_on_time_period(houses)

        self.houses_preprocessor.round_remained_high_values(houses)
        
        if export_path:
            self.builder.export_to_csv(houses, export_path)
        
        return houses

    def plot_house_consumption(self, house: House, month: Optional[int] = None, day: Optional[int] = None, time_range: Optional[tuple[str, str]] = None) -> None:
        if time_range:
            self.plotter.plot_consumption_over_time_range(house, time_range[0], time_range[1])
        else:
            self.plotter.plot_consumption_over_time(house, month=month, day=day)