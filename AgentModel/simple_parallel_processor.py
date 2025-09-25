import multiprocessing as mp
from typing import List, Dict
from AgentModel.house_model import HouseModel
from AgentModel.agent_statistics import AgentStatistics
from AgentModel.agent_maximum_simulation_steps import AgentSimulationSteps
from AgentModel.agents_ss_sc import AgentsSelfSufficiencySelfConsumption
from AgentModel.agent_types import AgentType

def run_scenario(args):
    houses, recommendation_dictionaries, number_of_houses, agent_type = args
    
    houses_to_simulate = houses[:number_of_houses]
    agent_model = HouseModel(n=number_of_houses, house_obj=houses_to_simulate, recommendation_dictionaries=recommendation_dictionaries, agent_type=agent_type)
    simulation_steps = AgentSimulationSteps(agent_model).get_maximum_simulation_steps(houses_to_simulate)
    agent_statistics_model = AgentStatistics(agent_model, simulation_steps)
    agent_statistics_model.run_simulation_and_generate_statistics()
    
    ss_sc_calculator = AgentsSelfSufficiencySelfConsumption(agent_model)
    sc = ss_sc_calculator.determine_simulated_self_consumption()
    ss = ss_sc_calculator.determine_simulated_self_sufficiency()
    
    return {
        'number_of_houses': number_of_houses,
        'agent_type': agent_type,
        'sc': sc,
        'ss': ss
    }

def process_scenarios_parallel(houses, recommendation_dictionaries, numbers_of_houses: List[int]) -> List[Dict]:    
    agent_type = AgentType.get_random_type()
    
    all_args = []
    for number in numbers_of_houses:
        all_args.append((houses, recommendation_dictionaries, number, agent_type))
        
    with mp.Pool() as pool:
        results = pool.map(run_scenario, all_args)
    
    return results