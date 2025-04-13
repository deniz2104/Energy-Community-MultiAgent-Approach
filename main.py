from housebuilder import HouseBuilder
from house import House
from solar_radiation_house import SolarRadiationHouse
from solar_radiation_house_builder import SolarRadiationHouseBuilder

if __name__ == "__main__":
    builder = HouseBuilder()
    
    houses = builder.build("consumption_data.csv")

    houses= builder.remove_houses_with_few_data_points(houses)

    houses= builder.remove_houses_with_lot_of_zeros(houses)

    houses= builder.resampling_houses_based_on_time_period(houses)

    builder.remove_anomalies_in_data(houses)

    builder.eliminate_days_after_a_year(houses)

    houses=builder.eliminate_houses_with_zero_for_a_period_of_time(houses)
    builder_solar_radiation = SolarRadiationHouseBuilder()
    solar_radiation_houses = builder_solar_radiation.build("solar_radiation_data.csv")
    solar_radiation_houses=builder_solar_radiation.match_and_filter_solar_houses(solar_radiation_houses, houses)

