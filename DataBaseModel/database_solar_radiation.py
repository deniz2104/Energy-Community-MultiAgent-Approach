
from DataBaseModel.database_core import DataHandler
from DataBaseModel.constants import SOLAR_DATA_FILE, SOLAR_VARIABLE_ID, ONE_YEAR_IN_SECONDS

class SolarRadiationDatabaseHandler(DataHandler):
    def extract_solar_radiation_data(self, file_name: str) -> None:
        house = self.tables['House']
        weather_data = self.tables['WeatherData']
        consumption = self.tables['Consumption']

        solar = weather_data[weather_data['WeatherVariableIDREF'] == SOLAR_VARIABLE_ID]
        grouped = solar.groupby(['WeatherStationIDREF', 'EpochTime'], as_index=False)['Value'].first()

        consumption_bounds = consumption.groupby('HouseIDREF')['EpochTime'].agg(StartingEpochTime='min', EndingEpochTime='max')

        merged = house[['ID', 'WeatherStationIDREF']].merge(grouped, on='WeatherStationIDREF')
        merged = merged.merge(consumption_bounds, left_on='ID', right_index=True)
        merged = merged[
            (merged['EpochTime'] >= merged['StartingEpochTime']) &
            (merged['EpochTime'] <= merged['EndingEpochTime']) &
            (merged['EpochTime'] < merged['StartingEpochTime'] + ONE_YEAR_IN_SECONDS)
        ]

        self.tables['House'] = house[house['ID'].isin(merged['ID'])]

        result = merged[['ID', 'EpochTime', 'Value']].rename(columns={'ID': 'HouseID', 'EpochTime': 'Timestamp', 'Value': 'TotalConsumption'})
        result = result.sort_values(['HouseID', 'Timestamp']).reset_index(drop=True)
        result = self.convert_epochtime_to_timestamp(result)
        self.export_to_csv(result, file_name)

if __name__ == "__main__":
    handler = SolarRadiationDatabaseHandler()
    handler.extract_solar_radiation_data(SOLAR_DATA_FILE)