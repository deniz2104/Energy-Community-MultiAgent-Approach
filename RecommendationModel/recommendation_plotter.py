import plotly.graph_objects as go
from plotly.subplots import make_subplots
from HelperFiles.file_to_handle_absolute_path_imports import *
from HelperFiles.hours_for_day_and_night import TOTAL_HOURS,NIGHT_HOURS

class RecommendationPlotter:
    def __init__(self):
        pass

    def plot_hours_recommendation_histogram(self, dictionary_of_recommendations_percentages_per_hour: dict[int, int]) -> None:
        hours_list = self._prepare_hours_data(dictionary_of_recommendations_percentages_per_hour)

        fig = self._create_histogram_figure(hours_list)
        fig = self._update_figure_layout(fig)
        
        fig.show()

    def plot_percentage_of_recommendation_per_appliance(self,dictionary_of_recommendation_percentage_per_appliance):
        fig = make_subplots(rows=1, cols=len(dictionary_of_recommendation_percentage_per_appliance), shared_xaxes=True, vertical_spacing=0.03)

        for i,(appliance_type, percentage) in enumerate(dictionary_of_recommendation_percentage_per_appliance.items()):
            fig.add_trace(go.Bar(x=[appliance_type], y=[percentage], name=appliance_type), row=1, col=i+1)

        fig.update_layout(title_text="Appliances Recommendation Percentages Over Time", showlegend=False)
        fig.show()

    def _prepare_hours_data(self, dictionary_of_recommendations_percentages_per_hour: dict[int, int]) -> list[int]:
        hours_list : list[int] = []

        for hour in range(TOTAL_HOURS):
            count = dictionary_of_recommendations_percentages_per_hour.get(hour, 0)
            if count > 0:
                hours_list.extend([hour] * int(count))

        return hours_list

    def _create_histogram_figure(self, hours_list: list[int]) -> go.Figure:
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
            )
        ])

    def _update_figure_layout(self, fig: go.Figure) -> go.Figure:
        fig.update_layout(
            title=dict(
                text="Usage Hours Distribution",
                x=0.5,
                font=dict(size=16, family="Arial, sans-serif")
            ),
            bargap=0.2)
        return fig
        