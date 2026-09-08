from typing import Callable
from HouseModel.house import House
from HouseModel.house_transforms import (
    count_zero_for_house,
    eliminate_anomalies_in_data,
    remove_houses_having_zero_for_a_period_of_time,
    round_remained_anomalies,
    resample_house,
)

Step = Callable[[list[House]], list[House]]

def apply_per_house(transform: Callable[[House], None]) -> Step:
    def step(houses: list[House]) -> list[House]:
        for house in houses:
            transform(house)
        return houses
    return step

def filter_houses(predicate: Callable[[House], bool]) -> Step:
    def step(houses: list[House]) -> list[House]:
        kept: list[House] = []
        for house in houses:
            if predicate(house):
                kept.append(house)
            else:
                type(house).unregister(house.house_id)
        return kept
    return step

def resampling_houses_based_on_time_period(houses: list[House]) -> list[House]:
    for house in houses:
        timestamps, consumption = resample_house(house)
        house.consumption = dict(zip(timestamps, consumption))
    return houses

# 50000 is programatically chosen as "at least 50% of the data is not psyhically present (timestamp is missing)"
remove_houses_with_few_data_points = filter_houses(lambda house: len(house.consumption) >= 50000)

# 15% is programatically chosen as "at least 15% of the data is zero, it would mess with our estimations, as a global rule, before counting for consective period"
remove_houses_with_lot_of_zeros = filter_houses(lambda house: count_zero_for_house(house) < 0.15 * len(house.consumption))

# we are keeping houses that do not have a period of 5 days with zero consumption, as it would mess with our estimations
eliminate_houses_with_zero_for_a_period_of_time = filter_houses(lambda house: remove_houses_having_zero_for_a_period_of_time(house) == 0)

PIPELINE: list[Step] = [
    remove_houses_with_few_data_points,
    remove_houses_with_lot_of_zeros,
    eliminate_houses_with_zero_for_a_period_of_time,
    apply_per_house(eliminate_anomalies_in_data),
    resampling_houses_based_on_time_period,
    apply_per_house(round_remained_anomalies),
]

def run(houses: list[House]) -> list[House]:
    for step in PIPELINE:
        houses = step(houses)
    return houses
