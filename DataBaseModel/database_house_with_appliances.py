from DataBaseModel.database_core import DataHandler
from DataBaseModel.constants import APPLIANCE_CONSUMPTION_DATA_FILE, ONE_YEAR_IN_SECONDS

class DatabaseHandlerAppliance(DataHandler):
    def extract_appliance_data(self,file_name: str) -> None:
        house = self.tables['House']
        consumption = self.tables['Consumption']
        appliance = self.tables['Appliance']
        appliance_type = self.tables['ApplianceType']

        grouped = consumption.groupby(['HouseIDREF', 'ApplianceIDREF', 'EpochTime'], as_index=False)['Value'].first()
        grouped = grouped.rename(columns={'Value': 'TotalConsumption'})

        starting_epoch_by_house = consumption.groupby('HouseIDREF')['EpochTime'].min()
        grouped = grouped.merge(starting_epoch_by_house.rename('StartingEpochTime'), left_on='HouseIDREF', right_index=True)
        grouped = grouped[grouped['EpochTime'] < grouped['StartingEpochTime'] + ONE_YEAR_IN_SECONDS]
        grouped = grouped.drop(columns='StartingEpochTime')

        merged = house[['ID']].merge(grouped, left_on='ID', right_on='HouseIDREF')
        self.tables['House'] = house[house['ID'].isin(merged['ID'])]

        merged = merged.merge(
            appliance[['ID', 'HouseIDREF', 'TypeIDREF']].rename(
                columns={'ID': 'ApplianceID', 'HouseIDREF': 'ApplianceHouseIDREF'}
            ),
            left_on=['ApplianceIDREF', 'HouseIDREF'], right_on=['ApplianceID', 'ApplianceHouseIDREF'],
        )
        merged = merged.merge(
            appliance_type.rename(columns={'ID': 'ApplianceTypeID', 'Name': 'Appliance_Name'}),
            left_on='TypeIDREF', right_on='ApplianceTypeID',
        )

        merged = merged.rename(columns={'ID': 'HouseID', 'ApplianceIDREF': 'Appliance_ID', 'EpochTime': 'Timestamp'})
        result = merged[['HouseID', 'Timestamp', 'Appliance_ID', 'Appliance_Name', 'TotalConsumption']]
        result = result.drop_duplicates().sort_values(['HouseID', 'Appliance_ID', 'Timestamp']).reset_index(drop=True)
        result = self.convert_epochtime_to_timestamp(result)
        result = self.export_to_csv(result, file_name)
        
if __name__ == "__main__":
    db_handler = DatabaseHandlerAppliance()
    db_handler.extract_appliance_data(APPLIANCE_CONSUMPTION_DATA_FILE)