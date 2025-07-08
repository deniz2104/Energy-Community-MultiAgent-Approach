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

