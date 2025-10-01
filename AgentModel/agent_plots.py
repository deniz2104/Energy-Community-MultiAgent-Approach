import plotly.graph_objects as go
from paretoset import paretoset
from plotly.subplots import make_subplots
from AgentModel.house_agent import HouseAgent
from AgentModel.agents_ss_sc import AgentsSelfSufficiencySelfConsumption

class AgentPlots:
    def __init__(self,model):
        self.model = model
        self.house_agents = [agent for agent in self.model.schedule.agents if isinstance(agent, HouseAgent)]
        self.self_consumption_and_self_sufficiency = AgentsSelfSufficiencySelfConsumption(model)

    def plot_self_consumption_and_sufficiency_comparison_with_savings(self, savings: float, number_of_houses: int) -> None:        
        simulated_self_consumption = [self.self_consumption_and_self_sufficiency.determine_simulated_self_consumption()]
        estimated_self_consumption = [self.self_consumption_and_self_sufficiency.determine_estimated_self_consumption()]

        simulated_self_sufficiency = [self.self_consumption_and_self_sufficiency.determine_simulated_self_sufficiency()]
        estimated_self_sufficiency = [self.self_consumption_and_self_sufficiency.determine_estimated_self_sufficiency()]

        agent_type = self.model.agent_type.value.title() if hasattr(self.model.agent_type, 'value') else str(self.model.agent_type).title()

        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Self-Consumption: Simulated vs Estimated', 'Self-Sufficiency: Simulated vs Estimated', 'Monetary Savings (RON)'),
            horizontal_spacing=0.20
        )
        
        fig.add_trace(
            go.Bar(y=simulated_self_consumption, name=f'{agent_type} - Simulated Self-Consumption', marker_color='lightblue'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(y=estimated_self_consumption, name=f'{agent_type} - Estimated Self-Consumption', marker_color='darkblue'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(y=simulated_self_sufficiency, name=f'{agent_type} - Simulated Self-Sufficiency', marker_color='lightgreen'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(y=estimated_self_sufficiency, name=f'{agent_type} - Estimated Self-Sufficiency', marker_color='darkgreen'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Bar(y=[savings], name=f'{agent_type} - Savings: RON{savings:.2f}', marker_color='gold'),
            row=1, col=3
        )
        
        fig.update_layout(
            title_text=f"{agent_type} Agent Analysis for {number_of_houses} Houses - Self-Consumption, Self-Sufficiency & Savings",
            showlegend=True,
            height=500,
            width=1200
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

    @staticmethod
    def plot_pareto_frontier(results_list):
        points = [(1-result['sc'], 1-result['ss']) for result in results_list]  
        pareto_mask = paretoset(points, sense=["max", "max"])
        pareto_points = [points[i] for i in range(len(points)) if pareto_mask[i]]
        pareto_points.sort(key=lambda p: p[0])

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=[p[0] for p in points],
            y=[p[1] for p in points],
            mode='markers',
            name='All Points',
            marker=dict(color='lightgrey', size=8)
        ))
        
        if pareto_points:
            fig.add_trace(go.Scatter(
                x=[p[0] for p in pareto_points],
                y=[p[1] for p in pareto_points],
                mode='lines+markers',
                name='Pareto Frontier',
                line=dict(color='red', width=2),
                marker=dict(color='red', size=10)
            ))

        fig.update_layout(
            title="Pareto Frontier Analysis",
            height=600,
            width=800
        )
        
        fig.show(renderer='browser')
    
    @staticmethod
    def plot_scenarios_results(results_list):
        fig = go.Figure()

        types_of_markers = {1: 'circle', 5: 'square', 10: 'diamond', 15: 'cross', 20: 'star', 23: 'triangle-up'}
        colors = {'ideal': 'green', 'enthusiastic': 'blue', 'non-enthusiastic': 'red'}

        for result in results_list:
            num_houses = result['number_of_houses']
            agent_type = result['agent_type']
            sc = result['sc']
            ss = result['ss']

            hover_text = f"Houses: {num_houses}<br>SC: {1-sc:.3f}<br>SS: {1-ss:.3f}<br>Agent Type: {agent_type}"

            fig.add_trace(go.Scatter(
                x=[1-sc],
                y=[1-ss],
                mode='markers',
                marker=dict(
                    color=colors.get(agent_type, 'gray'),
                    symbol=types_of_markers.get(num_houses, 'circle'),
                    size=10,
                    opacity=0.7
                ),
                text=f"{num_houses}",
                textposition="middle center",
                name=f'{num_houses} Houses - {agent_type}',
                hovertext=hover_text,
                hoverinfo="text",
                showlegend=num_houses not in [r['number_of_houses'] for r in results_list[:results_list.index(result)]]
            ))

        fig.update_layout(
            title="Self-Consumption vs Self-Sufficiency with Pareto Frontier",
            height=600,
            width=1000,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.01
            )
        )
        
        fig.show(renderer='browser')