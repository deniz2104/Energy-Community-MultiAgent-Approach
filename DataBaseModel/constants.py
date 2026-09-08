from pathlib import Path

from HouseModel.constants import YEAR_DAYS

REPO_ID: str = "denis210210/EnergeticCommunityData"

TABLE_FILENAMES: list[str] = [
    "Appliance.csv",
    "ApplianceType.csv",
    "Consumption.csv",
    "House.csv",
    "Record.csv",
    "WeatherData.csv",
    "WeatherStation.csv",
    "WeatherVariable.csv",
]

RAW_TABLES_DIR: Path = Path("CSVs") / "RawTables"
CONSUMPTION_DATA_DIR = Path("CSVs") / "RawConsumption"
CONSUMPTION_DATA_FILE = "house_consumption_data.csv"
SOLAR_DATA_FILE = "solar_radiation_data.csv"
APPLIANCE_CONSUMPTION_DATA_FILE = "appliance_consumption_data.csv"

SOLAR_VARIABLE_ID: int = 4
ONE_YEAR_IN_SECONDS: int = YEAR_DAYS * 24 * 60 * 60