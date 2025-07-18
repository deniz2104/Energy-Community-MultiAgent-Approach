import plotly.graph_objects as go
from plotly.subplots import make_subplots
class AppliancePlotter:
    def __init__(self):
        pass
    def plot_all_appliances_consumption_over_time(self,appliance):
        fig = make_subplots(rows=len(appliance.appliance_consumption), cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(appliance.appliance_consumption.items()):
            timestamps = [pair[0] for pair in consumption]
            values = [pair[1] for pair in consumption]
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i+1, col=1)

        fig.update_layout(title_text="Appliances Consumption Over Time", showlegend=False)
        fig.show()

    def plot_appliances_and_on_off_values(self,appliance,dictionary_with_on_off_values):
        fig = make_subplots(rows=len(appliance.appliance_consumption)*2, cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(appliance.appliance_consumption.items()):
            timestamps = [pair[0] for pair in consumption]
            values = [pair[1] for pair in consumption]
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i*2+1, col=1)
        
        for i, (appliance_type, points_of_interest) in enumerate(dictionary_with_on_off_values.items()):
            timestamps = [pair[0] for pair in points_of_interest]
            values = [pair[1] for pair in points_of_interest]
            fig.add_trace(go.Scatter(x=timestamps, y=values, mode='markers', name=f"{appliance_type} On and Off values", marker=dict(color='red')), row=i*2+2, col=1)
    
        fig.show()

    def plot_appliance_histogram(self, hours_dictionary, appliance_name=None, is_night=False):
        TOTAL_HOURS = 24
        NIGHT_HOURS = {0, 1, 2, 3, 4, 5, 6, 22, 23}

        hours_list = self._prepare_hours_data(hours_dictionary, NIGHT_HOURS, TOTAL_HOURS, is_night)

        fig = self._create_histogram_figure(hours_list, appliance_name)
        fig = self.update_figure_layout(fig, appliance_name)
        
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

    def update_figure_layout(self,fig,appliance_name=None):
        fig.update_layout(
            title=dict(
                text=f"Usage Hours Distribution - {appliance_name}" if appliance_name else "Appliance Usage Hours Distribution",
                x=0.5,
                font=dict(size=16, family="Arial, sans-serif")
            ),
            bargap=0.2)
        return fig
        