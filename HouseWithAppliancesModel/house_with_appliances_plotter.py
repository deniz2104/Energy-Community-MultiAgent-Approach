import plotly.graph_objects as go
from plotly.subplots import make_subplots
from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import TOTAL_HOURS,NIGHT_HOURS

class HouseWithAppliancesPlotter:
    def __init__(self):
        pass
    def plot_all_appliances_consumption_over_time(self,house_with_appliances):
        fig = make_subplots(rows=len(house_with_appliances.appliance_consumption), cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(house_with_appliances.appliance_consumption.items()):
            timestamps = [pair[0] for pair in consumption]
            values = [pair[1] for pair in consumption]
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i+1, col=1)

        fig.update_layout(title_text="Appliances Consumption Over Time", showlegend=False)
        fig.show()

    def plot_appliances_and_on_off_values(self,house_with_appliances,dictionary_with_on_off_values):
        fig = make_subplots(rows=len(house_with_appliances.appliance_consumption)*2, cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(house_with_appliances.appliance_consumption.items()):
            timestamps = [pair[0] for pair in consumption]
            values = [pair[1] for pair in consumption]
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i*2+1, col=1)
        
        for i, (appliance_type, on_off_points) in enumerate(dictionary_with_on_off_values.items()):
            timestamps_for_on_values = [pair[0] for pair in on_off_points if pair[1] == 1]
            on_values = [pair[1] for pair in on_off_points if pair[1] == 1]
            fig.add_trace(go.Scatter(x=timestamps_for_on_values, y=on_values, mode='markers', name=f"{appliance_type} On values", marker=dict(color='green')), row=i*2+2, col=1)

            timestamps_for_off_values = [pair[0] for pair in on_off_points if pair[1]==0] 
            off_values = [pair[1] for pair in on_off_points if pair[1]==0]
            fig.add_trace(go.Scatter(x=timestamps_for_off_values, y=off_values, mode='markers', name=f"{appliance_type} Off values", marker=dict(color='red')), row=i*2+2, col=1)   
        fig.show()

    def plot_appliance_histogram(self, hours_dictionary, appliance_name=None, is_night=False):
        hours_list = self._prepare_hours_data(hours_dictionary, NIGHT_HOURS, TOTAL_HOURS, is_night)

        fig = self._create_histogram_figure(hours_list, appliance_name)
        fig = self._update_figure_layout(fig, appliance_name)
        
        fig.show()
    
    def _prepare_hours_data(self, hours_dictionary, night_hours, total_hours,is_night=False):
        hours_list = []
        if is_night:
            all_hours = [hour for hour in range(total_hours) if hour in night_hours]
        else:
            all_hours = [hour for hour in range(total_hours) if hour not in night_hours]
        
        for hour in all_hours:
            count = hours_dictionary.get(hour, 0)
            if count > 0:
                hours_list.extend([hour] * int(count))
        
        return hours_list
    
    def _create_histogram_figure(self, hours_list, appliance_name):
        return go.Figure(data=[
            go.Histogram(
                x=hours_list,
                nbinsx=24,
                marker=dict(
                    color='rgba(55, 128, 191, 0.7)',
                    line=dict(
                        color='rgba(55, 128, 191, 1.0)', 
                        width=1
                    )
                ),
                name=f"{appliance_name} Usage" if appliance_name else "Appliance Usage"
            )
        ])

    def _update_figure_layout(self,fig,appliance_name=None):
        fig.update_layout(
            title=dict(
                text=f"Usage Hours Distribution - {appliance_name}" if appliance_name else "Appliance Usage Hours Distribution",
                x=0.5,
                font=dict(size=16, family="Arial, sans-serif")
            ),
            bargap=0.2)
        return fig
        