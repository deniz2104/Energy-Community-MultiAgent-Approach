import multiprocessing as mp
from typing import List, Dict
from AgentModel.house_model import HouseModel
from AgentModel.agent_maximum_simulation_steps import AgentSimulationSteps
from AgentModel.agents_ss_sc import AgentsSelfSufficiencySelfConsumption
from AgentModel.agent_types import AgentType
from AgentModel.agent_plots import AgentPlots
from AgentModel.agent_monetary_statistics import AgentMonetaryStatistics
from AgentModel.agent_run_model import RunModel


def run_scenario(args):
    houses, recommendation_dictionaries, number_of_houses, agent_type = args
    
    houses_to_simulate = houses[:number_of_houses]
    agent_model = HouseModel(n=number_of_houses, house_obj=houses_to_simulate, recommendation_dictionaries=recommendation_dictionaries, agent_type=agent_type)
    simulation_steps = AgentSimulationSteps(agent_model).get_maximum_simulation_steps(houses_to_simulate)
    
    run_model = RunModel(agent_model, simulation_steps)
    run_model.run()
    
    ss_sc_calculator = AgentsSelfSufficiencySelfConsumption(agent_model)
    sc = ss_sc_calculator.determine_simulated_self_consumption()
    ss = ss_sc_calculator.determine_simulated_self_sufficiency()
    
    monetary_stats = AgentMonetaryStatistics(agent_model, simulation_steps)
    savings = monetary_stats.simulated_savings()
    
    agent_plots = AgentPlots(agent_model)

    agent_plots.plot_self_consumption_and_sufficiency_comparison_with_savings(savings, number_of_houses)

    return {
        'number_of_houses': number_of_houses,
        'agent_type': agent_type,
        'sc': sc,
        'ss': ss,
        'savings': savings
    }

def process_scenarios_parallel(houses, recommendation_dictionaries, numbers_of_houses: List[int]) -> List[Dict]:    
    agent_types = AgentType.get_types()
    
    all_args = []
    for agent_type in agent_types:
        for number in numbers_of_houses:
            all_args.append((houses, recommendation_dictionaries, number, agent_type))
        
    with mp.Pool() as pool:
        results = pool.map(run_scenario, all_args)
    
    return results