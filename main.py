from HouseModel.house_facade import HouseFacade
from SolarRadiationModel.solar_radiation_house_facade import SolarRadiationHouseFacade
from PowerEstimatedModel.power_estimated_facade import PowerEstimatedFacade
from SelfConsumptionModel.determine_self_consumption_builder import SelfConsumptionBuilder
from SelfSufficiencyModel.determine_self_sufficiency_builder import SelfSufficiencyBuilder
from AppliancesModel.appliance_facade import ApplianceFacade
## thresholdul de 0.4 este unul arbitrar, dar nu am gasit un altul mai bun, sa vad daca pot sa il fac mai bun
## trebuie sa schimb denumirea de appliance (=> house_appliance_consumption)
## am de facut plot pentru distributia sigmoid a valorilor
## sa ma uit daca numele functiilor au sens si daca atributele si variabilele numite au si ele sens doar pt appliance
## sa tin cont de denumirile appliance urilor

## Trebuie sa generez in agent un nou profil generat
## Pot sa fac o scara cu un nivel de confidenta.
## 1 – toate appliance urile pornite
## Fiecarui appliance ii dau un scor. Fiecare au cate un punct la inceput. 
## Daca e acasa dau recomandare si daca nu e nu ii dau. Chestia asta o fac in functie de care sunt appliance urile dominante

## am de facut un requirments.txt
## am de facut si un venv
## type hints peste tot
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
    
    appliance_facade = ApplianceFacade()
    #appliances = appliance_facade.process_appliances_pipeline("CSVs/appliance_consumption_data.csv", houses, export_path="CSVs/appliance_consumption_preprocessed.csv")
    appliances = appliance_facade.builder.build("CSVs/appliance_consumption_preprocessed.csv")
    for appliance in appliances[:1]:
        appliance_facade.show_consumption_along_with_sigmoid_values(appliance)