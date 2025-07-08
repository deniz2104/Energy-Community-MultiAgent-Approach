from house_builder import HouseBuilder
from solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated_builder import PowerEstimatedBuilder
from determine_self_consumption_builder import SelfConsumptionBuilder
from determine_self_sufficiency_builder import SelfSufficiencyBuilder
from AppliancesModel.appliance_facade import ApplianceFacade
#from appliancebuilder import ApplianceBuilder
## trebuie sa vad niste chestii pentru numarul de panouri, putere per panou etc.
## ca sa vizualizez rezultatele, reprezentam consumul estimat in timp, productia estimata in timp, consumul simulat in timp (pe acelasi grafic),un calcul de autoconsum simulat/estimat, la fel si autonomie si recomandarile pe un grafic separat(bar chart)

## am de facut cate o clasa care face cate o chestie (plotter, procesare, nu fac mai multe lucruri intr o clasa))
## scopul va fi sa am mai multe foldere care fac cate un lucru (folder house in care am builder,model,processers...etc)
if __name__ == "__main__":
    house_builder = HouseBuilder()
    houses = house_builder.build("CSVs/houses_after_filtering_and_matching_with_weather_data.csv")

    solar_radiation_house_builder = SolarRadiationHouseBuilder()
    solar_radiation_house = solar_radiation_house_builder.build("CSVs/solar_radiation_after_resampling_and_matching_houses.csv")

    power_estimated_builder = PowerEstimatedBuilder()
    power_estimated = power_estimated_builder.build('CSVs/solar_radiation_after_resampling_and_matching_houses.csv')
    power_estimated_builder.determine_NEEG_for_all_houses(power_estimated)

    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption = self_consumption_builder.build_self_consumption(houses, power_estimated)
    
    self_sufficiency_builder = SelfSufficiencyBuilder()
    self_sufficiency_house = self_sufficiency_builder.build_self_sufficiency(houses, power_estimated)
    
    appliance_facade = ApplianceFacade()
    #appliances = appliance_facade.process_appliances_pipeline("CSVs/appliance_consumption_data.csv", houses, export_path="CSVs/appliance_consumption_preprocessed.csv")
    appliances = appliance_facade.builder.build("CSVs/appliance_consumption_preprocessed.csv")
