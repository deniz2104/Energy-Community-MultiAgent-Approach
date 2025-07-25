import pandas as pd
from sklearn.ensemble import IsolationForest
from scipy.stats.mstats import winsorize
import numpy as np
class HousePreprocessingData:
    def __init__(self):
        self.days_difference=12

    def eliminate_days_after_a_year_per_house(self,house):
        starting_date=min(pd.to_datetime(list(house.consumption.keys())))
        ending_date=max(pd.to_datetime(list(house.consumption.keys())))
        days_diff=ending_date-pd.Timedelta(days=(ending_date-starting_date).days - 365)
        if days_diff :
            timestamps_period=[t for t in pd.to_datetime(list(house.consumption.keys())) if t>=days_diff]
            self.consumption={t:v for t,v in house.consumption.items() if pd.Timestamp(t) not in timestamps_period}

    def eliminate_anomalies_in_data(self,house):
        df=pd.DataFrame(list(house.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp']=pd.to_datetime(df['Timestamp'])
        isolation_forest = IsolationForest(n_estimators=300,contamination=0.0002,random_state=42)
        isolation_forest.fit(df[['Consumption']])
        df['anomaly'] = isolation_forest.predict(df[['Consumption']])

        df=df[df['anomaly']==-1]
        val=df['Consumption'].values.tolist()
        house.consumption={t:v for t,v in house.consumption.items() if v not in val}

    def round_remained_anomalies(self,house):
        original_data = list(house.consumption.values())
        data = winsorize(np.array(original_data), limits=[0, 0.003])
        data = data.tolist()
        house.consumption = {k: v for k, v in zip(house.consumption.keys(), data)}

    def count_zero_for_house(self,house):
        return sum(value == 0 for value in house.consumption.values())

    def remove_houses_having_zero_for_a_period_of_time(self,house,is_appliance=None):
        first_period=None
        last_period=None
        time_stamps=set()
        if is_appliance is True:
            self.days_difference = 5
        for timestamp, value in house.consumption.items():
            if value == 0:
                if first_period is None:
                    first_period = timestamp
                last_period = timestamp
            else:
                if first_period and last_period:
                    days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
                    if days_diff >= self.days_difference:
                        time_stamps.add((first_period, last_period))
                first_period = None
                last_period = None

        if first_period and last_period:
            days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
            if days_diff >= self.days_difference:
                time_stamps.add((first_period, last_period))
        return len(time_stamps)