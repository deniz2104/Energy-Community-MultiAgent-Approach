import pandas as pd
class HouseStatistics:
    def __init__(self):
        pass

    def get_weekly_consumption_by_month(self,house):
        df = pd.DataFrame(list(house.consumption.items()), columns=['Timestamp', 'Consumption'])
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