from HouseModel.house_facade import HouseFacade
from SolarRadiationModel.solar_radiation_house_facade import SolarRadiationHouseFacade
from PowerEstimatedModel.power_estimated_facade import PowerEstimatedFacade
from SelfConsumptionModel.determine_self_consumption_builder import SelfConsumptionBuilder
from SelfSufficiencyModel.determine_self_sufficiency_builder import SelfSufficiencyBuilder
from AppliancesModel.appliance_facade import ApplianceFacade
## trebuie sa vad niste chestii pentru numarul de panouri, putere per panou etc.
## ca sa vizualizez rezultatele, reprezentam consumul estimat in timp, productia estimata in timp, consumul simulat in timp (pe acelasi grafic),un calcul de autoconsum simulat/estimat, la fel si autonomie si recomandarile pe un grafic separat(bar chart)
## as putea sa fac ceva o interfata pentru alea de plot basic si ala de filtrare
## ar trebui sa fac CSV-uri pentru fiecare casa cu appliance cu perioade on,off
if __name__ == "__main__":
    house_facade = HouseFacade()
    houses = house_facade.build_houses("CSVs/houses_after_filtering_and_matching_with_weather_data.csv")
    
    solar_radiation_house_facade = SolarRadiationHouseFacade()
    solar_radiation_houses = solar_radiation_house_facade.builder.build("CSVs/solar_radiation_after_resampling_and_matching_houses.csv")
    
    power_estimated_facade = PowerEstimatedFacade()
    power_estimated = power_estimated_facade.build_power_estimated_data('CSVs/solar_radiation_after_resampling_and_matching_houses.csv')
    power_estimated_facade.determine_NEEG_for_all_houses(power_estimated)

    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption = self_consumption_builder.build_self_consumption(houses, power_estimated)
    
    self_sufficiency_builder = SelfSufficiencyBuilder()
    self_sufficiency_house = self_sufficiency_builder.build_self_sufficiency(houses, power_estimated)
    
    appliance_facade = ApplianceFacade()
    #appliances = appliance_facade.process_appliances_pipeline("CSVs/appliance_consumption_data.csv", houses, export_path="CSVs/appliance_consumption_preprocessed.csv")
    appliances = appliance_facade.builder.build("CSVs/appliance_consumption_preprocessed.csv")
