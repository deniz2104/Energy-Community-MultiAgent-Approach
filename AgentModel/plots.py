import plotly.graph_objects as go
from plotly.subplots import make_subplots
from AgentModel.house_agent import HouseAgent

class AgentPlots:
    def __init__(self):
        pass
    
    def plot_self_consumption_and_sufficiency_comparison(self, house_agent: HouseAgent) -> None:

        agent_ids = [house_agent.unique_id]

        simulated_self_consumption = [house_agent.simulated_self_consumption]
        estimated_self_consumption = [house_agent.self_consumption]

        simulated_self_sufficiency = [house_agent.simulated_self_sufficiency]
        estimated_self_sufficiency = [house_agent.self_sufficiency]

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Self-Consumption: Simulated vs Estimated', 'Self-Sufficiency: Simulated vs Estimated')
        )
        
        fig.add_trace(
            go.Bar(x=agent_ids, y=simulated_self_consumption, name='Simulated Self-Consumption'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(x=agent_ids, y=estimated_self_consumption, name='Estimated Self-Consumption'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=agent_ids, y=simulated_self_sufficiency, name='Simulated Self-Sufficiency'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=agent_ids, y=estimated_self_sufficiency, name='Estimated Self-Sufficiency'),
            row=1, col=2
        )
        
        fig.update_layout(title_text="Agent Self-Consumption and Self-Sufficiency Comparison")
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