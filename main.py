from housebuilder import HouseBuilder
from solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated_builder import PowerEstimatedBuilder
from determine_self_consumption_builder import SelfConsumptionBuilder
from determine_self_sufficiency_builder import SelfSufficiencyBuilder
from appliancebuilder import ApplianceBuilder

## am de facut csv ul updatat 
## trebuie sa vad niste chestii pentru numarul de panouri, putere per panou etc.
## consider sub un anumit prag obersabil ca e oprit
## ma gandesc la o metoda prin care sa determin eventual o medie/ceva idk
## agent_type e basic ideal care primeste recomandare si reactioneaza intr-un anumit fel
## manager compara la fiecare moment de timp consumul estimat al casei respectiva cu productia estimata la acel moment de tip si ofera o recomandare la acel moment de timp
## la fiecare ora managerul da o recomandare si membrul reactioneaza la recomandare prin intermediul unei valori de consum simulat format pe baza consumului estimat ajutat cu 0.2
## ca sa vizualizez rezultatele, reprezentam consumul estimat in timp, productia estimata in timp, consumul simulat in timp (pe acelasi grafic),un calcul de autoconsum simulat/estimat, la fel si autonomie si recomandarile pe un grafic separat(bar chart)

if __name__ == "__main__":
    house_builder = HouseBuilder()
    houses = house_builder.build('houses_after_filtering_and_matching_with_weather_data.csv')

    solar_radiation_house_builder = SolarRadiationHouseBuilder()
    solar_radiation_house = solar_radiation_house_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    
    power_estimated_builder = PowerEstimatedBuilder()
    power_estimated = power_estimated_builder.build('solar_radiation_after_resampling_and_matching_houses.csv')
    
    self_consumption_builder = SelfConsumptionBuilder()
    self_consumption = self_consumption_builder.build_self_consumption(houses, power_estimated)

    self_sufficiency_builder = SelfSufficiencyBuilder()
    self_sufficiency_house = self_sufficiency_builder.build_self_sufficiency(houses, power_estimated)

    appliances_builder = ApplianceBuilder()
    appliances=appliances_builder.build("appliance_consumption_preprocessed.csv")
        