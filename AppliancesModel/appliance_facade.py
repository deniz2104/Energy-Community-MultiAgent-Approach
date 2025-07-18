from .appliance_builder import ApplianceBuilder
from .appliance_preprocessing_data import AppliancePreprocessingData
from .appliance_hours_weights import ApplianceHoursWeights
from .appliance_resampling import ApplianceResampling
from .appliance_plotter import AppliancePlotter
from .appliance_label_for_on_and_off_values import ApplianceOnOffValues
from HelperFiles.file_to_handle_absolute_path_imports import *

class ApplianceFacade:
    def __init__(self):
        self.builder = ApplianceBuilder()
        self.preprocessor = AppliancePreprocessingData()
        self.resampler = ApplianceResampling()
        self.plotter = AppliancePlotter()
        self.data_labeler = ApplianceOnOffValues()
        self.calculate_weights = ApplianceHoursWeights()

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
        on_off_dict=self.data_labeler.determine_on_off_periods(appliance)
        return on_off_dict

    def show_hours_distribution(self, appliance):
        on_off_dict = self.data_labeler.determine_on_off_periods(appliance)
        hours_distribution = self.data_labeler.count_on_off_values_per_time_period(on_off_dict)
        return hours_distribution

    def plot_appliances_and_on_off_values(self, appliance, on_off_dict, plot_on_off=True):
        self.plotter.plot_all_appliances_consumption_over_time(appliance)
        if plot_on_off and on_off_dict is not None:
            self.plotter.plot_appliances_and_on_off_values(appliance,on_off_dict)

    def show_hours_weights(self,appliance):
        hours_distribution = self.show_hours_distribution(appliance)
        hours_weights = self.calculate_weights.determine_hours_weights(hours_distribution)
        return hours_weights

    def show_appliance_histogram(self, appliance):
        hours_distribution = self.show_hours_distribution(appliance)
        for appliance_name, hours in hours_distribution.items():
            self.plotter.plot_appliance_histogram(hours,appliance_name)
