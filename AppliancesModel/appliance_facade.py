from .appliance_builder import ApplianceBuilder
from .appliance_preprocessing_data import AppliancePreprocessingData
from .appliance_resampling import ApplianceResampling
from .appliance_plotter import AppliancePlotter
from .appliance_label_for_on_and_off_values import ApplianceOnOffValues
from HelperFiles.file_to_handle_absolute_path_imports import *

##Am de facut csv cu perioadele de on si off pentru fiecare tip de appliance, pentru fiecare casa

class ApplianceFacade:
    def __init__(self):
        self.builder = ApplianceBuilder()
        self.preprocessor = AppliancePreprocessingData()
        self.resampler = ApplianceResampling()
        self.plotter = AppliancePlotter()
        self.data_labeler = ApplianceOnOffValues()

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
        night_period=self.data_labeler.determine_off_hours_for_every_appliance_at_day_and_night(on_off_dict)
        day_period=self.data_labeler.determine_on_hours_for_every_appliance_at_day_and_night(on_off_dict,day_values=True)
        return on_off_dict, night_period, day_period

    def plot_appliances_and_on_off_values(self, appliance, on_off_dict, plot_on_off=True):
        self.plotter.plot_all_appliances_consumption_over_time(appliance)
        if plot_on_off and on_off_dict is not None:
            self.plotter.plot_appliances_and_on_off_values(appliance,on_off_dict)
