from EnergyDataScrapperModel.all_data_scrapping import give_5_best_offers_related_to_current_offer
from AgentModel.agent_monetary_statistics import AgentMonetaryStatistics
import plotly.graph_objects as go
import plotly.subplots as sp

class CommunityMonetarySavings(AgentMonetaryStatistics):
    def __init__(self, agent_model, simulation_steps, all_companies_data=None):
        super().__init__(agent_model, simulation_steps)
        self._all_companies_data = all_companies_data

    def get_better_prices_and_renewable_energy_options(self):
        if not self.agent_model.energetic_company_provider:
            raise ValueError("No energetic company provider found in the model")
        
        current_company_name = next(iter(self.agent_model.energetic_company_provider.keys()))
        better_5_companies = give_5_best_offers_related_to_current_offer(current_company_name)
        return better_5_companies
        
    def calculate_savings_for_better_companies(self):
        better_companies = self.get_better_prices_and_renewable_energy_options()
        savings_data = {}
        
        for company_name, company_data in better_companies:
            price_per_kwh = float(company_data.get('price_of_kW', 0.0))
            
            savings = self.simulated_savings(change_provider=True, new_price_per_kwh=price_per_kwh)
            
            savings_data[company_name] = {
                'savings': float(savings),
                'price_per_kwh': price_per_kwh,
                'renewable_percentage': float(company_data.get('renewal_energy_percentage', 0))
            }
        return savings_data

    def plot_community_savings_by_companies(self):
        savings_data = self.calculate_savings_for_better_companies()
        
        if not savings_data:
            print("No better companies found to compare savings.")
            return
        
        companies = list(savings_data.keys())
        savings = [float(data['savings']) for data in savings_data.values()]
        renewable_percentages = [float(data['renewable_percentage']) for data in savings_data.values()]
        
        fig = sp.make_subplots(
            rows=2, cols=1,
            subplot_titles=('Community Monetary Savings by Energy Company', 
                          'Renewable Energy Percentage by Company'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Bar(
                x=companies,
                y=savings,
                name='Savings',
                marker_color='skyblue',
                text=[f'{s:.2f}' for s in savings],
                textposition='outside',
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=companies,
                y=renewable_percentages,
                name='Renewable Energy',
                marker_color='lightgreen',
                text=[f'{r:.1f}%' for r in renewable_percentages],
                textposition='outside',
                showlegend=False
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=800,
            title_text="Community Energy Analysis",
            title_x=0.5,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Energy Companies", row=1, col=1)
        fig.update_xaxes(title_text="Energy Companies", row=2, col=1)
        
        fig.update_yaxes(title_text="Money Saved (Currency Units)", row=1, col=1)
        fig.update_yaxes(title_text="Renewable Energy Percentage (%)", row=2, col=1)

        fig.show(renderer='browser')
