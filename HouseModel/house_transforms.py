import pandas as pd
from sklearn.ensemble import IsolationForest
from scipy.stats.mstats import winsorize
import numpy as np
from typing import Optional
from HouseModel.house import House
from HouseModel.constants import DIFFERENCE_DAYS, N_ESTIMATORS, CONTAMINATION, SEED, INFERIOR_WINSORIZE_LIMITS

def eliminate_anomalies_in_data(house: House) -> None:
    timestamps, values = house.timestamps, house.consumption_values
    isolation_forest = IsolationForest(n_estimators=N_ESTIMATORS, contamination=CONTAMINATION, random_state=SEED)
    predictions = isolation_forest.fit_predict(np.array(values).reshape(-1, 1))
    house.consumption = {t: v for t, v, prediction in zip(timestamps, values, predictions) if prediction != -1}

def round_remained_anomalies(house: House) -> None:
    winsorized = winsorize(np.array(house.consumption_values), limits=INFERIOR_WINSORIZE_LIMITS)
    house.consumption = dict(zip(house.timestamps, winsorized.tolist()))

def count_zero_for_house(house: House) -> int:
    return sum(value == 0 for value in house.consumption_values)

def remove_houses_having_zero_for_a_period_of_time(house: House, is_appliance: Optional[bool] = None) -> int:
    days_difference = 5 if is_appliance else DIFFERENCE_DAYS
    first_period: Optional[str] = None
    last_period: Optional[str] = None
    zero_periods: set[tuple[str, str]] = set()

    def record_period_if_long_enough() -> None:
        if first_period and last_period:
            days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
            if days_diff >= days_difference:
                zero_periods.add((first_period, last_period))

    for timestamp, value in house.consumption.items():
        if value == 0:
            first_period = first_period or timestamp
            last_period = timestamp
        else:
            record_period_if_long_enough()
            first_period, last_period = None, None

    record_period_if_long_enough()
    return len(zero_periods)

def resample_house(house: House) -> tuple[list[str], list[float]]:
    df = pd.DataFrame({'Timestamp': house.timestamps, 'Consumption': house.consumption_values})
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index('Timestamp').sort_index()

    df_hourly = df.resample('h').mean().dropna()
    timestamps = df_hourly.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
    consumption = df_hourly['Consumption'].tolist()
    return timestamps, consumption
