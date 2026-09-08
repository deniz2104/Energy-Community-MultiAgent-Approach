from typing import Optional
from HouseModel.house import House
from HouseModel.house_pipeline import run as run_preprocessing_pipeline
from HouseModel.house_plotter import HousePlotter
from CsvModel.csv_core import export_to_csv

_plotter = HousePlotter()

def process_houses_pipeline(csv_path: str, export_path: str) -> list[House]:
    houses = House.build(csv_path)
    houses = run_preprocessing_pipeline(houses)

    export_to_csv(House.houses_data_to_rows(), export_path)

    return houses

def plot_house_consumption(house: House, month: Optional[int] = None, day: Optional[int] = None, time_range: Optional[tuple[str, str]] = None) -> None:
    if time_range:
        _plotter.plot_consumption_over_time_range(house, time_range[0], time_range[1])
    else:
        _plotter.plot_consumption_over_time(house, month=month, day=day)
