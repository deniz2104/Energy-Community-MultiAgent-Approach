from AgentModel.agents_ss_sc import AgentsSelfSufficiencySelfConsumption
from AgentModel.house_agent import HouseAgent
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class HouseAgentMonetarySavings(AgentsSelfSufficiencySelfConsumption):
    def __init__(self, agent_model):
        super().__init__(agent_model)
        self.house_agents = [agent for agent in self.agent_model.schedule.agents if isinstance(agent, HouseAgent)]

    def plot_most_impacted_houses(self, result):
        houses_to_show = {5: 3, 10: 5, 15: 7, 20: 9, 23: 11}
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Self-Consumption Differences', 'Self-Sufficiency Differences'),
            vertical_spacing=0.15
        )
        
        num_houses = result['number_of_houses']
        agent_type = result['agent_type']

        if num_houses not in houses_to_show:
            return

        agent_model = result['agent_model']
        house_agents = [agent for agent in agent_model.schedule.agents if isinstance(agent, HouseAgent)]

        list_of_ss_and_sc_diffs = []
        for agent in house_agents:
            sc_diff = abs(self.determine_simulated_self_consumption() - agent.self_consumption)
            ss_diff = abs(self.determine_simulated_self_sufficiency() - agent.self_sufficiency)
            list_of_ss_and_sc_diffs.append((sc_diff, ss_diff, agent.unique_id))

        list_of_ss_and_sc_diffs.sort(key=lambda x: x[0] + x[1], reverse=True)
        top_impacted_houses = list_of_ss_and_sc_diffs[:houses_to_show[num_houses]]

        x_labels = [f"House{tuple_with_sc_and_ss_data[2]}" for tuple_with_sc_and_ss_data in top_impacted_houses]
        sc_diffs = [tuple_with_sc_and_ss_data[0] * 100 for tuple_with_sc_and_ss_data in top_impacted_houses]
        ss_diffs = [tuple_with_sc_and_ss_data[1] * 100 for tuple_with_sc_and_ss_data in top_impacted_houses]

        fig.add_trace(
            go.Bar(
                x=x_labels,
                y=sc_diffs,
                name=f'{num_houses} houses - {agent_type}',
                legendgroup=f'{num_houses}-{agent_type}'
            ),
            row=1, col=1
        )
            
        fig.add_trace(
            go.Bar(
                x=x_labels,
                y=ss_diffs,
                name=f'{num_houses} houses - {agent_type}',
                legendgroup=f'{num_houses}-{agent_type}',
                showlegend=False
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="House ID", row=2, col=1)
        fig.update_yaxes(title_text="Difference (%)", row=1, col=1)
        fig.update_yaxes(title_text="Difference (%)", row=2, col=1)
        
        fig.update_layout(
            height=900,
            title_text="Impact on Most Affected Houses: Current vs Simulated Metrics",
            barmode='group',
            showlegend=True
        )
        
        fig.show(renderer='browser')
