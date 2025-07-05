import pandas as pd
from appliance import Appliance
class ApplianceResampling:
    def __init__(self):
        pass

    def resampling_appliance_data(self, appliances):
        resampled_appliances = {}
        for appliance in appliances:
            resampled_appliance = Appliance(appliance.house_id)
            resampled_appliances[appliance.house_id] = resampled_appliance
            
            for appliance_type, pairs in appliance.consumption.items():
                
                df = pd.DataFrame(pairs, columns=['timestamp', 'consumption'])
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.set_index('timestamp', inplace=True)
                
                df_hourly = df.resample('h')['consumption'].mean().reset_index()
                
                for _, row in df_hourly.iterrows():
                    resampled_appliance.add_appliance_consumption(
                        row['timestamp'], appliance_type, row['consumption'])
                
                if appliance_type in resampled_appliance.consumption:
                    sorted_consumption = sorted(resampled_appliance.consumption[appliance_type], 
                                            key=lambda x: x[0])
                    resampled_appliance.consumption[appliance_type] = sorted_consumption
        
        return list(resampled_appliances.values())