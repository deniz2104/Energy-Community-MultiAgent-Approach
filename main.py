import sqlite3
import csv
import time
from collections import OrderedDict
import plotly.express as px
from sklearn.ensemble import IsolationForest 
import pandas as pd


class DatabaseHandler():
    def __init__(self):
        pass
    def read_database(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
    def extract_data(self):
        self.cursor.execute("""
            SELECT h.ID, cs.EpochTime, cs.TotalValue
            FROM House h
            JOIN (
                SELECT HouseIDREF, EpochTime, SUM(Value) AS TotalValue
                FROM Consumption
                GROUP BY HouseIDREF, EpochTime
            ) cs ON cs.HouseIDREF = h.ID
            ORDER BY h.ID;
        """)
        rows = self.cursor.fetchall()
        rows=list(rows)
        for i in range(len(rows)):
            row=list(rows[i])
            row[1]=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(row[1]))
            rows[i]=tuple(row)
        return rows

    def write_to_csv(self, data, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime', 'TotalValue'])
            writer.writerows(data)

    def close_connection(self):
        self.connection.close()


class House():
    def __init__(self, house_id):
        self.house_id = house_id
        self.consumption = {}
    def add_consumption(self, timestamp, value):
        self.consumption[timestamp] = value

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
            fig = px.scatter(x=pd.to_datetime(list(self.consumption.keys())), y=list(self.consumption.values()), title=f'House ID: {self.house_id}')
            fig.show()
        if month is not None and day is None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day('month', month)
            fig = px.scatter(x=timestamps_period, y=consumption_period, title=f'House ID: {self.house_id}')
            fig.show()
        if month is None and day is not None:
            timestamps_period, consumption_period = self.filter_values_by_month_and_day('day', day)
            fig = px.scatter(x=timestamps_period, y=consumption_period, title=f'House ID: {self.house_id}')
            fig.show()
    
    def plot_consumption_over_time_range(self, time_stamp_1, time_stamp_2):
        time_stamp_1=pd.to_datetime(time_stamp_1)
        time_stamp_2=pd.to_datetime(time_stamp_2)
        timestamps_period=[t for t in pd.to_datetime(list(self.consumption.keys())) if time_stamp_1<=t<=time_stamp_2]
        consumption_period=[self.consumption[t] for t in timestamps_period]
        fig = px.scatter(x=timestamps_period, y=consumption_period, title=f'House ID: {self.house_id}')
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


    def count_zero_for_house(self):
        return sum(value == 0 for value in self.consumption.values())

    def remove_houses_having_zero_for_a_period_of_time(self):
        first_period=None
        last_period=None
        time_stamps=set()
        count=0
        for timestamp, value in self.consumption.items():
            if value == 0:
                if first_period is None:
                    first_period = timestamp
                last_period = timestamp
            else:
                if first_period and last_period:
                    days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
                    if days_diff >= 14:
                        time_stamps.add((first_period, last_period))
                first_period = None
                last_period = None

        if first_period and last_period:
            days_diff = (pd.to_datetime(last_period) - pd.to_datetime(first_period)).days
            if days_diff >= 14:
                time_stamps.add((first_period, last_period))
        if(len(time_stamps) > 0):
            print(f"House {self.house_id} has {len(time_stamps)} periods of zeros ≥ 14 days")
            for first, last in time_stamps:
                print(f"  Period: {first} to {last}, {(pd.to_datetime(last) - pd.to_datetime(first)).days} days")
            count=1
            return count
        return "pula"

class HouseBuilder(House) :
    def __init__(self):
        pass
    def build(self, csv_path):
        houses = {}

        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                timestamp = row['EpochTime']
                value = float(row['TotalValue'])

                if house_id not in houses:
                    houses[house_id] = House(house_id)

                houses[house_id].add_consumption(timestamp, value)

        return list(houses.values())

    def resampling_houses_based_on_time_period(self, houses):
        resampled_houses={}
        for house in houses:
            df=pd.DataFrame(list(house.consumption.items()), columns=['Timestamp', 'Consumption'])
            df['Timestamp']=pd.to_datetime(df['Timestamp'])
            df.set_index('Timestamp', inplace=True)
            df.sort_index(inplace=True)

            df_hourly=df.resample('h').mean()
            timestamps=df_hourly.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
            consumption=df_hourly['Consumption'].tolist()
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
        houses_with_no_eliminated_houses = [house for house in houses if house.remove_houses_having_zero_for_a_period_of_time()=="pula"]
        return list(houses_with_no_eliminated_houses)



if __name__ == "__main__":
    builder = HouseBuilder()
    
    houses = builder.build("consumption_data.csv")

    houses= builder.remove_houses_with_few_data_points(houses)

    houses= builder.remove_houses_with_lot_of_zeros(houses)

    houses= builder.resampling_houses_based_on_time_period(houses)

    builder.remove_anomalies_in_data(houses)

    builder.eliminate_days_after_a_year(houses)

    houses=builder.eliminate_houses_with_zero_for_a_period_of_time(houses)
