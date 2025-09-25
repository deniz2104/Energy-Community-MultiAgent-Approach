import plotly.graph_objects as go
from plotly.subplots import make_subplots
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption

class HouseWithAppliancesPlotter:
    def __init__(self) -> None:
        pass

    def plot_all_appliances_consumption_over_time(self, house_with_appliances: HouseWithAppliancesConsumption) -> None:
        fig = make_subplots(rows=len(house_with_appliances.appliance_consumption), cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(house_with_appliances.appliance_consumption.items()):
            timestamps = list(consumption.keys())
            values = list(consumption.values())
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i+1, col=1)

        fig.update_layout(title_text="Appliances Consumption Over Time", showlegend=False)
        fig.show(renderer='browser')
        