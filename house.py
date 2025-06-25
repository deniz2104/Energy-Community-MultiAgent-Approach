import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import IsolationForest 
from scipy.stats.mstats import winsorize

class House():
    def __init__(self, house_id):
        self.house_id = house_id
        self.consumption = {}
    def add_consumption(self, timestamp, value):
        self.consumption[timestamp] = value

    def prepare_house_for_resampling(self):
        df=pd.DataFrame(list(self.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp']=pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        df.sort_index(inplace=True)

        df_hourly=df.resample('h').mean()
        timestamps=df_hourly.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        consumption=df_hourly['Consumption'].tolist()
        return timestamps, consumption
    
    def show_starting_time_and_ending_time(self):
        timestamps=list(self.consumption.keys())
        if not timestamps:
            print('No consumption data available.')
            return None, None   
        return timestamps[0],timestamps[-1]

    def filter_values_by_month_and_day(self, mode, value):
        timestamps=[]
        consumptions=[]

        for key,consumption in self.consumption.items():
            timestamp=pd.to_datetime(key)
            if(mode=='month' and timestamp.month==value) or (mode=='day' and timestamp.day==value):
                timestamps.append(timestamp)
                consumptions.append(consumption)
        return timestamps, consumptions

    def plot_consumption_over_time(self,month=None,day=None):
        if month is None and day is None:
            fig = px.line(x=pd.to_datetime(list(self.consumption.keys())), y=list(self.consumption.values()), title=f'House ID: {self.house_id}')
            fig.show()
        if month is not None and day is None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day('month', month)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {self.house_id}')
            fig.show()
        if month is None and day is not None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day('day', day)
            fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {self.house_id}')
            fig.show()
    
    def plot_consumption_over_time_range(self, time_stamp_1, time_stamp_2):
        time_stamp_1=pd.to_datetime(time_stamp_1)
        time_stamp_2=pd.to_datetime(time_stamp_2)
        timestamps_period=[t for t in pd.to_datetime(list(self.consumption.keys())) if time_stamp_1<=t<=time_stamp_2]
        consumption_period=[self.consumption[t] for t in timestamps_period]
        fig = px.line(x=timestamps_period, y=consumption_period, title=f'House ID: {self.house_id}')
        fig.show()

    def eliminate_days_after_a_year_per_house(self):
        starting_date=min(pd.to_datetime(list(self.consumption.keys())))
        ending_date=max(pd.to_datetime(list(self.consumption.keys())))
        days_diff=ending_date-pd.Timedelta(days=(ending_date-starting_date).days - 365)
        if days_diff :
            timestamps_period=[t for t in pd.to_datetime(list(self.consumption.keys())) if t>=days_diff]
            self.consumption={t:v for t,v in self.consumption.items() if pd.Timestamp(t) not in timestamps_period}

    def eliminate_anomalies_in_data(self):
        df=pd.DataFrame(list(self.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp']=pd.to_datetime(df['Timestamp'])
        isolation_forest = IsolationForest(n_estimators=300,contamination=0.0002,random_state=42)
        isolation_forest.fit(df[['Consumption']])
        df['anomaly'] = isolation_forest.predict(df[['Consumption']])

        df=df[df['anomaly']==-1]
        val=df['Consumption'].values.tolist()
        self.consumption={t:v for t,v in self.consumption.items() if v not in val}
    def get_monthly_consumption(self):
        df = pd.DataFrame(list(self.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        monthly_avg = df.groupby(pd.Grouper(freq='ME'))['Consumption'].mean()
        for timestamp, value in monthly_avg.items():
            print(f"Month: {timestamp.strftime('%Y-%m')}, Average Consumption: {value:.2f}")
    def get_weekly_consumption_by_month(self):
        df = pd.DataFrame(list(self.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        
        df['Month'] = df.index.strftime('%Y-%m')
        
        weekly_stats = df.groupby(['Month', pd.Grouper(freq='W')])['Consumption'].mean()
        
        current_month = None
        for month,value in weekly_stats.items():
            if month != current_month:
                print(f"\n=== Month: {month} ===")
                current_month = month
            print(f"Week: {month[1].strftime('%Y-%m-%d')}, Average Consumption: {value:.2f}")
            
    def filtrate_remained_anomalies(self):
        original_data = list(self.consumption.values())
        data = winsorize(np.array(original_data), limits=[0, 0.003])
        data = data.tolist()
        self.consumption = {k: v for k, v in zip(self.consumption.keys(), data)}

    def count_zero_for_house(self):
        return sum(value == 0 for value in self.consumption.values())

    def remove_houses_having_zero_for_a_period_of_time(self,is_appliance=None,days_difference=12):
        first_period=None
        last_period=None
        time_stamps=set()
        if is_appliance is True:
            days_difference = 5
        for timestamp, value in self.consumption.items():
            if value == 0:
                if first_period is None:
                    first_period = timestamp
                last_period = timestamp
            else:
                if first_period and last_period:
                    days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
                    if days_diff >= days_difference:
                        time_stamps.add((first_period, last_period))
                first_period = None
                last_period = None

        if first_period and last_period:
            days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
            if days_diff >= days_difference:
                time_stamps.add((first_period, last_period))
        return len(time_stamps)