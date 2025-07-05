from housebuilder import HouseBuilder
from solar_radiation_house_builder import SolarRadiationHouseBuilder
from power_estimated_builder import PowerEstimatedBuilder
from determine_self_consumption_builder import SelfConsumptionBuilder
from determine_self_sufficiency_builder import SelfSufficiencyBuilder
from appliancebuilder import ApplianceBuilder
## am de important din folderul de CSV-uri de acum in: appliancebuilder.py,
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

    appliances_builder = ApplianceBuilder()
    appliances=appliances_builder.build("CSVs/appliance_consumption_preprocessed.csv")
    for appliance in appliances[:1]:
        temporary_dict = appliance.determine_on_off_periods()
        appliance.plot_appliances_and_on_off_values(temporary_dict)
        night_period = appliance.determine_off_hours_for_every_appliance_at_day_and_night(temporary_dict)
        day_period = appliance.determine_off_hours_for_every_appliance_at_day_and_night(temporary_dict, day_values=True)
        print(night_period)
        print(day_period)