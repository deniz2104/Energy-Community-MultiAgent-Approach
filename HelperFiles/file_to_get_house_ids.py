from HouseModel.house_builder import HouseBuilder

house_builder = HouseBuilder()
houses = house_builder.build('houses_after_filtering_and_matching_with_weather_data.csv')
house_ids=[house.house_id for house in houses]
