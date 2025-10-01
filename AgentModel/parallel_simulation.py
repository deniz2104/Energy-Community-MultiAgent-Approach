import multiprocessing as mp
from typing import List, Dict
from AgentModel.agent_plots import AgentPlots
from AgentModel.house_model import HouseModel
from AgentModel.agent_maximum_simulation_steps import AgentSimulationSteps
from AgentModel.agents_ss_sc import AgentsSelfSufficiencySelfConsumption
from AgentModel.agent_types import AgentType
from AgentModel.agent_monetary_statistics import AgentMonetaryStatistics
from AgentModel.community_monetary_savings import CommunityMonetarySavings
from AgentModel.agent_plots_monetary_savings import HouseAgentMonetarySavings
from AgentModel.agent_run_model import RunModel
from AgentModel.get_random_company_provider import get_random_company_provider
from EnergyDataScrapperModel.all_data_scrapping import get_best_companies_data_from_the_response
from HouseModel.house import House


def run_scenario(args):
    houses, recommendation_dictionaries, number_of_houses, agent_type, energetic_company_provider, all_companies_data = args
    
    houses_to_simulate = houses[:number_of_houses]
    agent_model = HouseModel(n=number_of_houses, house_obj=houses_to_simulate, recommendation_dictionaries=recommendation_dictionaries, agent_type=agent_type, energetic_company_provider=energetic_company_provider)
    simulation_steps = AgentSimulationSteps(agent_model).get_maximum_simulation_steps(houses_to_simulate)
    
    run_model = RunModel(agent_model, simulation_steps)
    run_model.run()
    
    ss_sc_calculator = AgentsSelfSufficiencySelfConsumption(agent_model)
    sc = ss_sc_calculator.determine_simulated_self_consumption()
    ss = ss_sc_calculator.determine_simulated_self_sufficiency()
    
    monetary_stats = AgentMonetaryStatistics(agent_model, simulation_steps)
    savings = monetary_stats.simulated_savings()

    community_savings = CommunityMonetarySavings(agent_model, simulation_steps, all_companies_data)
    community_savings_data = community_savings.calculate_savings_for_better_companies()
    
    return {
        'number_of_houses': number_of_houses,
        'agent_type': agent_type,
        'sc': sc,
        'ss': ss,
        'savings': savings,
        'community_savings_data': community_savings_data,
        'agent_model': agent_model,
        'simulation_steps': simulation_steps
    }

def generate_plots_for_results(results: List[Dict], companies_data) -> None:
 
    for result in results:
        number_of_houses = result['number_of_houses']
        savings = result['savings']
        
        if 'agent_model' in result:
            agent_plots = AgentPlots(result['agent_model'])
            agent_plots.plot_self_consumption_and_sufficiency_comparison_with_savings(savings, number_of_houses)
        
        if 'community_savings_data' in result and result['community_savings_data']:
            if 'agent_model' in result and 'simulation_steps' in result:
                community_savings = CommunityMonetarySavings(
                    result['agent_model'], 
                    result['simulation_steps'], 
                    companies_data
                )
                community_savings.plot_community_savings_by_companies()
        HouseAgentMonetarySavings(result['agent_model']).plot_most_impacted_houses(result)

def process_scenarios_parallel(houses, recommendation_dictionaries, numbers_of_houses: List[int]) -> List[Dict]:    
    agent_types = AgentType.get_types()
    company_provider = get_random_company_provider()

    if not company_provider:
        raise ValueError("No company provider available.")
    
    all_companies_data = get_best_companies_data_from_the_response()
    
    all_args = []
    for agent_type in agent_types:
        for number in numbers_of_houses:
            all_args.append((houses, recommendation_dictionaries, number, agent_type, company_provider, all_companies_data))
    
    with mp.Pool() as pool:
        results = pool.map(run_scenario, all_args)
    
    generate_plots_for_results(results, all_companies_data)
    
    return results