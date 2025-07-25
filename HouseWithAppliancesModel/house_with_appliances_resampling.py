import pandas as pd
from .house_with_appliances import HouseWithAppliancesConsumption

class HouseWithAppliancesResampling:
    def __init__(self) -> None:
        pass

    def resampling_appliance_data(self, houses_with_appliances: list[HouseWithAppliancesConsumption]) -> list[HouseWithAppliancesConsumption]:
        resampled_houses_with_appliances: dict[str, HouseWithAppliancesConsumption] = {}
        for house in houses_with_appliances:
            resampled_appliance = HouseWithAppliancesConsumption(house.house_id)
            resampled_houses_with_appliances[house.house_id] = resampled_appliance
            
            for appliance_type, pairs in house.appliance_consumption.items():
                
                df = pd.DataFrame(pairs, columns=['timestamp', 'consumption'])
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.set_index('timestamp', inplace=True)
                
                df_hourly = df.resample('h')['consumption'].mean().reset_index()
                
                for _, row in df_hourly.iterrows():
                    resampled_appliance.add_appliance_consumption(
                        row['timestamp'], appliance_type, row['consumption'])
                
                if appliance_type in resampled_appliance.appliance_consumption:
                    sorted_consumption = sorted(resampled_appliance.appliance_consumption[appliance_type], 
                                            key=lambda x: x[0])
                    resampled_appliance.appliance_consumption[appliance_type] = sorted_consumption
        
        return list(resampled_houses_with_appliances.values())