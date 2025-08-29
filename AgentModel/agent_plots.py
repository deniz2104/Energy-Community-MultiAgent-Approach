import plotly.graph_objects as go
from plotly.subplots import make_subplots
from AgentModel.house_agent import HouseAgent
from AgentModel.agents_ss_sc import AgentsSelfSufficiencySelfConsumption

class AgentPlots:
    def __init__(self,model):
        self.model = model
        self.house_agents = [agent for agent in self.model.schedule.agents if isinstance(agent, HouseAgent)]
        self.self_consumption_and_self_sufficiency = AgentsSelfSufficiencySelfConsumption(model)

    def plot_self_consumption_and_sufficiency_comparison(self) -> None:

        simulated_self_consumption = [self.self_consumption_and_self_sufficiency.determine_simulated_self_consumption()]
        estimated_self_consumption = [self.self_consumption_and_self_sufficiency.determine_estimated_self_consumption()]

        simulated_self_sufficiency = [self.self_consumption_and_self_sufficiency.determine_simulated_self_sufficiency()]
        estimated_self_sufficiency = [self.self_consumption_and_self_sufficiency.determine_estimated_self_sufficiency()]

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Self-Consumption: Simulated vs Estimated', 'Self-Sufficiency: Simulated vs Estimated')
        )
        
        fig.add_trace(
            go.Bar(y=simulated_self_consumption, name='Simulated Self-Consumption'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(y=estimated_self_consumption, name='Estimated Self-Consumption'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(y=simulated_self_sufficiency, name='Simulated Self-Sufficiency'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(y=estimated_self_sufficiency, name='Estimated Self-Sufficiency'),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Agent Self-Consumption and Self-Sufficiency Comparison",
            showlegend=True,
            height=500
        )
        fig.show(renderer='browser')

    def plot_consumption_time_series(self, house_agent: HouseAgent) -> None:
        steps=min(len(house_agent.base_consumption),len(house_agent.reference_consumption),len(house_agent.simulated_consumption))
        base_steps = list(house_agent.base_consumption.keys())[:steps]
        base_values = list(house_agent.base_consumption.values())[:steps]

        ref_values = list(house_agent.reference_consumption.values())[:steps]

        sim_values = list(house_agent.simulated_consumption.values())[:steps]

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=base_steps, y=base_values, name='Base Consumption (Production)'))
        fig.add_trace(go.Scatter(x=base_steps, y=ref_values, name='Reference Consumption'))
        fig.add_trace(go.Scatter(x=base_steps, y=sim_values, name='Simulated Consumption'))

        fig.update_layout(title=f'Agent {house_agent.unique_id}: Consumption Time Series')
        fig.show(renderer='browser')

    def plot_self_consumption_sufficiency_scatter(self) -> None :
        estimated_x = [1 - agent.self_consumption for agent in self.house_agents]
        estimated_y = [1 - agent.self_sufficiency for agent in self.house_agents]
        
        simulated_x = [1 - agent.simulated_self_consumption for agent in self.house_agents]
        simulated_y = [1 - agent.simulated_self_sufficiency for agent in self.house_agents]
        
        house_ids = [agent.unique_id for agent in self.house_agents]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=estimated_x,
            y=estimated_y,
            mode='markers',
            name='Estimated Values',
            marker=dict(
                size=10,
                color='blue',
                opacity=0.7
            ),
            text=[f'House ID: {house_id}' for house_id in house_ids],
            hovertemplate='<b>%{text}</b><br>' +
                         '1 - Self Consumption: %{x:.3f}<br>' +
                         '1 - Self Sufficiency: %{y:.3f}<br>' +
                         '<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=simulated_x,
            y=simulated_y,
            mode='markers',
            name='Simulated Values',
            marker=dict(
                size=10,
                color='red',
                opacity=0.7
            ),
            text=[f'House ID: {house_id}' for house_id in house_ids],
            hovertemplate='<b>%{text}</b><br>' +
                         '1 - Self Consumption: %{x:.3f}<br>' +
                         '1 - Self Sufficiency: %{y:.3f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, 
                     annotation_text="Perfect Self-Sufficiency")
        fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5,
                     annotation_text="Perfect Self-Consumption")
        
        fig.update_layout(
            title="Scatter Plot: House Profiles - Distance from Perfect Energy Autonomy",
            xaxis_title="1 - Self Consumption (Distance from Perfect Self-Consumption)",
            yaxis_title="1 - Self Sufficiency (Distance from Perfect Self-Sufficiency)",
            showlegend=True,
            height=600,
            width=800,
            hovermode='closest'
        )
        
        #fig.add_annotation(
        #    x=0, y=0,
        #    text="Ideal Point<br>(Perfect Autonomy)",
        #    showarrow=True,
        #    arrowhead=2,
        #    arrowsize=1,
        #    arrowwidth=2,
        #    arrowcolor="green",
        #    ax=50,
        #    ay=-50,
        #    bgcolor="lightgreen",
        #    opacity=0.8
        #)
        
        fig.show(renderer='browser')