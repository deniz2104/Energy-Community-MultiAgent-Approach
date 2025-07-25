import pandas as pd
from typing import Optional
from .house import House

class HouseStatistics:
    def __init__(self) -> None:
        pass

    def get_weekly_consumption_by_month(self, house: House) -> None:
        df = pd.DataFrame(list(house.consumption.items()), columns=['Timestamp', 'Consumption'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        
        df['Month'] = df.index.strftime('%Y-%m')
        
        weekly_stats = df.groupby(['Month', pd.Grouper(freq='W')])['Consumption'].mean()
        
        current_month: Optional[str] = None
        for month, value in weekly_stats.items():
            if month != current_month:
                print(f"\n=== Month: {month} ===")
                current_month = month
            print(f"Week: {month[1].strftime('%Y-%m-%d')}, Average Consumption: {value:.2f}")