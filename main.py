from HouseModel.house_facade import HouseFacade
from SolarRadiationModel.solar_radiation_house_facade import SolarRadiationHouseFacade
from PowerEstimatedModel.power_estimated_facade import PowerEstimatedFacade
from SelfConsumptionModel.determine_self_consumption_builder import SelfConsumptionBuilder
from SelfSufficiencyModel.determine_self_sufficiency_builder import SelfSufficiencyBuilder
from HouseWithAppliancesModel.house_with_appliances_facade import HouseWithAppliancesFacade
## sa nu uit sa fac dictionar din lista de dictionare => dictionar de dictionare => sa nu mai convertesc lista la dictionar si sa pot face .get pe el

## Trebuie sa generez in agent un nou profil generat
## Pot sa fac o scara cu un nivel de confidenta.
## 1 – toate appliance urile pornite
## Fiecarui appliance ii dau un scor. Fiecare au cate un punct la inceput. 
## Daca e acasa dau recomandare si daca nu e nu ii dau. Chestia asta o fac in functie de care sunt appliance urile dominante
## la final ar fi good practice sa fac si un __init__.py si un devcontainer

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

    house_with_appliances_facade = HouseWithAppliancesFacade()
    #appliances = appliance_facade.process_appliances_pipeline("CSVs/appliance_consumption_data.csv", houses, export_path="CSVs/appliance_consumption_preprocessed.csv")
    houses_with_appliances = house_with_appliances_facade.builder.build("CSVs/appliance_consumption_preprocessed.csv")
    for house in houses_with_appliances[:3]:
        house_with_appliances_facade.plot_appliances_and_on_off_values(house)
        list_of_appliances = house_with_appliances_facade.determine_appliances_with_highest_consumption(house)
        print(list_of_appliances)