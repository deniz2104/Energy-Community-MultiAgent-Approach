from DataBaseModel.database_core import DataHandler
from DataBaseModel.constants import CONSUMPTION_DATA_FILE, SOLAR_VARIABLE_ID, ONE_YEAR_IN_SECONDS

class HouseDatabaseHandler(DataHandler):
    def extract_house_consumption_data(self, file_name: str) -> None:
        house = self.tables['House']
        consumption = self.tables['Consumption']
        weather_data = self.tables['WeatherData']

        solar = weather_data[weather_data['WeatherVariableIDREF'] == SOLAR_VARIABLE_ID]
        solar_house_ids = set(house[['ID', 'WeatherStationIDREF']].merge(solar, on='WeatherStationIDREF')['ID'])

        grouped = consumption.groupby(['HouseIDREF', 'EpochTime'], as_index=False)['Value'].sum()

        merged = house[['ID']].merge(grouped, left_on='ID', right_on='HouseIDREF')
        merged = merged[merged['ID'].isin(solar_house_ids)]

        starting_epoch_per_house = merged.groupby('ID')['EpochTime'].transform('min')
        merged = merged[merged['EpochTime'] < starting_epoch_per_house + ONE_YEAR_IN_SECONDS]

        self.tables['House'] = house[house['ID'].isin(merged['ID'])]

        result = merged[['ID', 'EpochTime', 'Value']].rename(columns={'ID': 'HouseID', 'EpochTime': 'Timestamp', 'Value': 'TotalConsumption'})
        result = result.sort_values(['HouseID', 'Timestamp']).reset_index(drop=True)
        result = self.convert_epochtime_to_timestamp(result)
        self.export_to_csv(result, file_name)

if __name__ == "__main__":
    db_handler = HouseDatabaseHandler()
    db_handler.extract_house_consumption_data(CONSUMPTION_DATA_FILE)