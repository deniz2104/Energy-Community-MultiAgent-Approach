from .house_with_appliances_builder import HouseWithAppliancesBuilder
from .house_with_appliances_preprocessing_data import HouseWithAppliancesPreprocessingData
from .house_with_appliances_resampling import HouseWithAppliancesResampling
from .house_with_appliances_plotter import HouseWithAppliancesPlotter
from .house_with_appliances_statistics import HouseWithAppliancesStatistics
from .house_with_appliances_label_for_on_and_off_values import HouseWithAppliancesOnOffValues
from .determine_which_appliance_consumes_more import DetermineWhichApplianceConsumesMore
from HelperFiles.file_to_handle_absolute_path_imports import *

class HouseWithAppliancesFacade:
    def __init__(self):
        self.builder = HouseWithAppliancesBuilder()
        self.preprocessor = HouseWithAppliancesPreprocessingData()
        self.resampler = HouseWithAppliancesResampling()
        self.plotter = HouseWithAppliancesPlotter()
        self.data_labeler = HouseWithAppliancesOnOffValues()
        self.statistics = HouseWithAppliancesStatistics()
        self.determine_which_appliance_consumes_more = DetermineWhichApplianceConsumesMore()


    def build_appliances(self, csv_path):
        return self.builder.build(csv_path)

    def process_appliances_pipeline(self,csv_path,houses,export_path=None):
        appliances = self.build_appliances(csv_path)
                
        appliances = self.resampler.resampling_appliance_data(appliances)

        self.preprocessor.matching_timestamps_between_appliance_and_house(appliances, houses)
        
        self.preprocessor.remove_appliances_with_zero_data(appliances)
        
        self.preprocessor.eliminate_anomalies_in_appliances(appliances)

        self.preprocessor.eliminate_appliances_with_five_days_of_no_consumption(appliances)
        
        if export_path:
            self.builder.export_to_csv(appliances, export_path)

        return appliances

    def see_on_off_patterns(self,appliance):
        return self.data_labeler.determine_on_off_periods(appliance)

    def show_hours_distribution(self, appliance):
        on_off_dict = self.data_labeler.determine_on_off_periods(appliance)
        return self.data_labeler.count_on_off_values_per_time_period(on_off_dict)

    def plot_appliances_and_on_off_values(self, appliance, on_off_dict=None, plot_on_off=True):
        self.plotter.plot_all_appliances_consumption_over_time(appliance)
        if plot_on_off and on_off_dict is not None:
            self.plotter.plot_appliances_and_on_off_values(appliance,on_off_dict)

    def show_hours_weights(self,appliance):
        hours_distribution = self.show_hours_distribution(appliance)
        return self.statistics.determine_hours_weights(hours_distribution)

    def show_appliance_histogram(self, appliance):
        hours_distribution = self.show_hours_distribution(appliance)
        for appliance_name, hours in hours_distribution.items():
            self.plotter.plot_appliance_histogram(hours,appliance_name)

    def show_appliance_mean_consumption_based_on_hour(self,appliance):
        on_off_dict = self.see_on_off_patterns(appliance)
        hours_distribution = self.show_hours_distribution(appliance)
        return self.statistics.get_mean_consumption_by_hour(appliance,on_off_dict,hours_distribution)

    def show_consumption_along_with_sigmoid_values(self, appliance):
        self.determine_which_appliance_consumes_more.show_sigmoid_values_along_with_consumption_values(appliance)