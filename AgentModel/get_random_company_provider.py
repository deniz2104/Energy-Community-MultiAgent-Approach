from EnergyDataScrapperModel.all_data_scrapping import get_best_companies_data_from_the_response
import random

def get_random_company_provider():
    all_data = get_best_companies_data_from_the_response()
    if not all_data:
        return None
    key, value = random.choice(list(all_data.items()))
    return {key: value}