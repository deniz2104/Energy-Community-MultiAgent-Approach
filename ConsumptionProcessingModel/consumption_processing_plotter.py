from typing import Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from HelperFiles.hours_for_day_and_night import TOTAL_HOURS, NIGHT_HOURS
from HouseWithAppliancesModel.house_with_appliances import HouseWithAppliancesConsumption

class ConsumptionProcessingPlotter:
    """
    Plotter class for consumption processing, on/off patterns, and analysis visualizations.
    Handles plotting of consumption patterns, histograms, and on/off value distributions.
    """
    
    def __init__(self) -> None:
        pass

    def plot_appliances_and_on_off_values(self, house_with_appliances: HouseWithAppliancesConsumption, dictionary_with_on_off_values: dict[str, dict[str, int]]) -> None:
        """
        Plot appliances consumption data along with their detected on/off patterns.
        
        Args:
            house_with_appliances: House with appliance consumption data
            dictionary_with_on_off_values: Dictionary mapping appliances to their on/off states by timestamp
        """
        fig = make_subplots(rows=len(house_with_appliances.appliance_consumption)*2, cols=1, shared_xaxes=True, vertical_spacing=0.03)

        for i, (appliance_type, consumption) in enumerate(house_with_appliances.appliance_consumption.items()):
            timestamps = list(consumption.keys())
            values = list(consumption.values())
            fig.add_trace(go.Scatter(x=timestamps, y=values, name=appliance_type), row=i*2+1, col=1)
        
        for i, (appliance_type, on_off_points) in enumerate(dictionary_with_on_off_values.items()):
            timestamps_for_on_values = [timestamp for timestamp, value in on_off_points.items() if value == 1]
            on_values = [value for value in on_off_points.values() if value == 1]
            fig.add_trace(go.Scatter(x=timestamps_for_on_values, y=on_values, mode='markers', name=f"{appliance_type} On values", marker=dict(color='green')), row=i*2+2, col=1)

            timestamps_for_off_values = [timestamp for timestamp, value in on_off_points.items() if value == 0]
            off_values = [value for value in on_off_points.values() if value == 0]
            fig.add_trace(go.Scatter(x=timestamps_for_off_values, y=off_values, mode='markers', name=f"{appliance_type} Off values", marker=dict(color='red')), row=i*2+2, col=1)   
        fig.show()

    def plot_appliance_histogram(self, hours_dictionary: dict[int, int], appliance_name: Optional[str] = None, is_night: bool = False) -> None:
        """
        Plot histogram of appliance usage hours distribution.
        
        Args:
            hours_dictionary: Dictionary mapping hours to usage counts
            appliance_name: Name of the appliance for plot title
            is_night: Whether to focus on night hours or day hours
        """
        hours_list = self._prepare_hours_data(hours_dictionary, is_night)

        fig = self._create_histogram_figure(hours_list, appliance_name)
        fig = self._update_figure_layout(fig, appliance_name, is_night)
        
        fig.show()

    def _prepare_hours_data(self, hours_dictionary: dict[int, int], is_night: bool = False) -> list[int]:
        """
        Prepare hours data for histogram plotting based on day/night filter.
        
        Args:
            hours_dictionary: Dictionary mapping hours to usage counts
            is_night: Whether to focus on night hours or day hours
            
        Returns:
            List of hours repeated by their usage counts
        """
        hours_list: list[int] = []
        target_hours = NIGHT_HOURS if is_night else {h for h in range(TOTAL_HOURS) if h not in NIGHT_HOURS}

        for hour in target_hours:
            count = hours_dictionary.get(hour, 0)
            if count > 0:
                hours_list.extend([hour] * int(count))
        
        return hours_list

    def _create_histogram_figure(self, hours_list: list[int], appliance_name: Optional[str] = None) -> go.Figure:
        """
        Create the histogram figure with proper styling.
        
        Args:
            hours_list: List of hours data for histogram
            appliance_name: Name of appliance for legend
            
        Returns:
            Configured Plotly figure
        """
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

    def _update_figure_layout(self, fig: go.Figure, appliance_name: Optional[str] = None, is_night: bool = False) -> go.Figure:
        """
        Update figure layout with titles and formatting.
        
        Args:
            fig: Plotly figure to update
            appliance_name: Name of appliance for title
            is_night: Whether showing night or day hours
            
        Returns:
            Updated figure with proper layout
        """
        period = "Night" if is_night else "Day"
        title = f"{period} Usage Hours Distribution"
        if appliance_name:
            title = f"{title} - {appliance_name}"
            
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=16, family="Arial, sans-serif")
            ),
            xaxis_title="Hour of Day",
            yaxis_title="Usage Count",
            bargap=0.2
        )
        return fig