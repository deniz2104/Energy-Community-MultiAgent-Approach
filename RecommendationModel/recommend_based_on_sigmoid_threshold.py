import pandas as pd
from HouseWithAppliancesModel.consumption_data_processor import ConsumptionDataProcessor
from HelperFiles.hours_for_day_and_night import TOTAL_HOURS
class RecommendationModel:
    def __init__(self):
        self.threshold = None
        self.helper_file= ConsumptionDataProcessor()

    def make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(self,house_with_appliances):
        consumption_for_each_appliance= self.helper_file.gather_consumption_values_for_each_appliance(house_with_appliances)
        sigmoid_values_for_each_appliance= self.helper_file.determine_sigmoid_values_for_each_appliance(consumption_for_each_appliance)
        consumption_mapped_to_sigmoid_values = {}
        for appliance_name, _ in consumption_for_each_appliance.items():
            if appliance_name not in consumption_mapped_to_sigmoid_values:
                consumption_mapped_to_sigmoid_values[appliance_name] = dict(zip(consumption_for_each_appliance[appliance_name], sigmoid_values_for_each_appliance[appliance_name]))
        return consumption_mapped_to_sigmoid_values
    
    def see_how_many_reccommendations_are_going_to_be_made(self, house_with_appliances, appliance_thresholds):
        consumption_mapped_to_sigmoid_values = self.make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(house_with_appliances)
        number_of_recommendations = {}
        for appliance_name, consumption_dict in consumption_mapped_to_sigmoid_values.items():
            for _, sigmoid_value in consumption_dict.items():
                if sigmoid_value >= appliance_thresholds.get(appliance_name, 0):
                    number_of_recommendations[appliance_name] = number_of_recommendations.get(appliance_name, 0) + 1
        return number_of_recommendations

    def make_percentage_of_recommendations(self,house_with_appliances, appliance_thresholds):
        number_of_recommendations = self.see_how_many_reccommendations_are_going_to_be_made(house_with_appliances, appliance_thresholds)
        percentage_of_recommendations = {}
        consumption_for_each_appliance= self.helper_file.gather_consumption_values_for_each_appliance(house_with_appliances)
        for appliance_name,_ in consumption_for_each_appliance.items():
            total_consumption = len(consumption_for_each_appliance[appliance_name])
            if total_consumption > 0:
                percentage_of_recommendations[appliance_name] = (number_of_recommendations.get(appliance_name, 0) / total_consumption) * 100
        return percentage_of_recommendations
    
    def make_distribution_per_hour_per_appliance(self,house_with_appliances, appliance_thresholds):
        hour_dictionary = {}
        dictionary_of_consumption_and_sigmoid_values = self.make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(house_with_appliances)
        for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
            hours_count = {hour: 0 for hour in range(TOTAL_HOURS)}
            total_consumption_per_hour = {hour: 0 for hour in range(TOTAL_HOURS)}
            
            for timestamp, value in consumption.items():
                hour = pd.to_datetime(timestamp).hour
                total_consumption_per_hour[hour] += 1
                
                if dictionary_of_consumption_and_sigmoid_values[appliance_type].get(value,0) >= appliance_thresholds.get(appliance_type, 0):
                    hours_count[hour] += 1
            
            hour_percentages = {
                hour: (hours_count[hour] / total_consumption_per_hour[hour]) * 100
                for hour in range(TOTAL_HOURS)
                if total_consumption_per_hour[hour] > 0 and hours_count[hour] > 0
            }
            
            hour_dictionary[appliance_type] = hour_percentages
        return hour_dictionary
    
    def get_timestamp(self, house_with_appliances):
        
        first_appliance = next(iter(house_with_appliances.appliance_consumption.values()))
        return list(first_appliance.keys())
    
    def give_recommendation_based_on_sigmoid_threshold(self, house_with_appliances, appliance_thresholds):
        whole_timestamp = self.get_timestamp(house_with_appliances)
        count_recommendation = 0
        self.threshold = len(appliance_thresholds) // 2 + len(appliance_thresholds) % 2  # Ensure threshold is an integer
        print(self.threshold)
        dictionary_of_consumption_along_with_sigmoid = self.make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(house_with_appliances)
        
        for timestamp in whole_timestamp:
            count_of_appliances = 0
            for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
                consumption_value = consumption.get(timestamp, 0)  # Get the consumption value for this timestamp
                sigmoid_value = dictionary_of_consumption_along_with_sigmoid[appliance_type].get(consumption_value, 0)
                
                if sigmoid_value >= appliance_thresholds.get(appliance_type, 0):
                    count_of_appliances += 1
                    
            if count_of_appliances >= self.threshold:
                count_recommendation += 1
        return count_recommendation
    
    def see_hour_distribution_per_given_recommendation(self,house_with_appliances,appliance_thresholds):
        hour_distribution = {hour: 0 for hour in range(TOTAL_HOURS)}
        total_hour_distribution = {hour: 0 for hour in range(TOTAL_HOURS)}
        whole_timestamp = self.get_timestamp(house_with_appliances)
        self.threshold = len(appliance_thresholds) // 2 + len(appliance_thresholds) % 2  # Ensure threshold is an integer
        dictionary_of_consumption_along_with_sigmoid = self.make_dictionary_from_consumption_and_sigmoid_values_for_each_appliance(house_with_appliances)

        for timestamp in whole_timestamp:
            count_of_appliances = 0
            hour = pd.to_datetime(timestamp).hour
            total_hour_distribution[hour] += 1
            for appliance_type, consumption in house_with_appliances.appliance_consumption.items():
                consumption_value = consumption.get(timestamp, 0)
                sigmoid_value = dictionary_of_consumption_along_with_sigmoid[appliance_type].get(consumption_value, 0)

                if sigmoid_value >= appliance_thresholds.get(appliance_type, 0):
                    count_of_appliances += 1

            if count_of_appliances >= self.threshold:
                hour_distribution[hour] += 1

        return total_hour_distribution, hour_distribution

    def make_percentage_of_overall_recommendations(self, house_with_appliances, appliance_thresholds):
        number_of_recommendation = self.give_recommendation_based_on_sigmoid_threshold(house_with_appliances, appliance_thresholds)
        total_timestamps = len(self.get_timestamp(house_with_appliances))
        return (number_of_recommendation / total_timestamps) * 100

    def make_dictionary_of_percentages_per_hour(self, house_with_appliances, appliance_thresholds):
        total_hour_distribution, hour_distribution = self.see_hour_distribution_per_given_recommendation(house_with_appliances, appliance_thresholds)

        return {
            hour: (count / total_hour_distribution[hour] * 100) if total_hour_distribution[hour] > 0 else 0
            for hour, count in hour_distribution.items()
        }