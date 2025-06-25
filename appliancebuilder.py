import csv
from appliance import Appliance
from housebuilder import HouseBuilder
import pandas as pd
class ApplianceBuilder():
    def __init__(self):
        pass
    
    def open_csv_file(self, csv_path):
        results=[]
        with open(csv_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                house_id = int(row['HouseID'])
                timestamp = row['EpochTime']
                appliance_name = row['Appliance_Name']
                value = float(row['TotalValue'])
                results.append((house_id, timestamp,appliance_name,value))
        return results

    def export_to_csv(self, appliances, file_path):
         with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HouseID', 'EpochTime','Appliance_Name','TotalValue'])
            for appliance in appliances:
                for appliance_name,pairs in appliance.consumption.items():
                    for timestamp, value in pairs:
                        writer.writerow([appliance.house_id, timestamp,appliance_name,value])

    def build(self, csv_path):
        appliances ={}
        rows=self.open_csv_file(csv_path)
        for house_id, timestamp, appliance_name, value in rows:
            if house_id not in appliances:
                appliances[house_id] = Appliance(house_id)

            appliances[house_id].add_appliance_consumption(timestamp, appliance_name, value)
        return list(appliances.values())
    def matching_timestamps_between_appliance_and_house(self, appliances,consumption_houses):
        consumption_dict = {house.house_id: house for house in consumption_houses}
    
        for appliance in appliances:
            if appliance.house_id in consumption_dict:
                consumption_house = consumption_dict[appliance.house_id]
                appliance.eliminate_days_after_a_year(consumption_house)

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
    def remove_appliances_with_zero_data(self, appliances):
        for appliance in appliances:
            appliance.eliminate_appliances_with_lot_of_zeros_consumption()
    
    def eliminate_anomalies_in_appliances(self, appliances):
        for appliance in appliances:
            appliance.eliminate_anomalies_in_my_data()

    def eliminate_appliance_with_five_days_of_no_consumption(self, appliances):
        for appliance in appliances:
            appliance.eliminate_appliance_with_five_days_of_no_consumption()
    
if __name__ == "__main__":
    builder=ApplianceBuilder()
    appliances=builder.build("appliance_consumption_data.csv")
    house_builder=HouseBuilder()
    houses=house_builder.build("houses_after_filtering_and_matching_with_weather_data.csv")
    builder.matching_timestamps_between_appliance_and_house(appliances, houses)
    appliances=builder.resampling_appliance_data(appliances)
    builder.remove_appliances_with_zero_data(appliances)
    builder.eliminate_anomalies_in_appliances(appliances)
    builder.eliminate_appliance_with_five_days_of_no_consumption(appliances)
    builder.export_to_csv(appliances, "appliance_consumption_preprocessed.csv")