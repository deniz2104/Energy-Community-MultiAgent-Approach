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

    consumption_house_ids = {house.house_id for house in houses}
    solar_house_ids = {house.house_id for house in solar_radiation_houses}
    
    common_house_ids = consumption_house_ids.intersection(solar_house_ids)
    print(f"Houses in both datasets: {len(common_house_ids)}")
    
    houses = [house for house in houses if house.house_id in common_house_ids]
    solar_radiation_houses = [house for house in solar_radiation_houses if house.house_id in common_house_ids]
    
    builder_solar_radiation.match_and_filter_solar_houses(solar_radiation_houses, houses)
