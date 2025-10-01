import requests
import datetime
from EnergyDataScrapperModel.get_parameters_for_scrapper import GetTypeOffer,GetTypeProduct
from EnergyDataScrapperModel.zone_scrapping import get_zone_id_based_on_current_location

def set_params():
    params = {
    "request": "comparator-electric",
    "tip_oferta": GetTypeOffer.ORICARE.value,
    "data_start_aplicare": datetime.datetime.now().strftime("%Y-%m-%d"),
    "tip_client": "casnic",
    "tip_pret": "nediferentiat",
    "nivel_tensiune": "JT_",
    "id_zona": ""+str(get_zone_id_based_on_current_location()),
    "tip_produs": GetTypeProduct.ORICARE.value
    }
    return params

def get_data():
    url = "https://posf.ro/api/v1/comparator"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}, params=set_params())
    return response.json()

def make_price_of_kW_per_company(company):
    base_price = float(company.get("pret_energie", 0)) + float(company.get("acciza", 0)) + float(company.get("contravaloare_certificate_verzi", 0)) + float(company.get("tarif_serviciu_distributie", 0)) + float(company.get("tarif_serviciu_sistem", 0)) + float(company.get("tarif_transport_tl", 0)) + float(company.get("taxa_cogenerare_inalta_eficienta", 0))
    return round((base_price + (base_price * float(company.get("tva", 0)) / 100)), 2)

def get_best_companies_data_from_the_response():
    all_companies = get_data()
    relevant_data = {}
    for company in all_companies:
        if company["nume_furnizor"] not in relevant_data:
            relevant_data[company["nume_furnizor"]] = {
                "renewal_energy_percentage": company.get("procent_energie_surse_regenerabile", 0),
                "price_of_kW": make_price_of_kW_per_company(company)
            }
        else:
            existing_price = relevant_data[company["nume_furnizor"]]["price_of_kW"]
            existing_renewable_energy = relevant_data[company["nume_furnizor"]]["renewal_energy_percentage"]
            
            new_price = make_price_of_kW_per_company(company)
            new_renewable_energy = company.get("procent_energie_surse_regenerabile", 0)

            if new_price < existing_price and new_renewable_energy >= existing_renewable_energy:
                relevant_data[company["nume_furnizor"]]["price_of_kW"] = new_price
                relevant_data[company["nume_furnizor"]]["renewal_energy_percentage"] = new_renewable_energy

    return relevant_data

def give_5_best_offers_related_to_current_offer(current_company:str):
    all_data = get_best_companies_data_from_the_response()
    if current_company not in list(all_data.keys()):
        raise ValueError(f"Current company '{current_company}' not found in the data.")
    
    current_offer = all_data[current_company]
    current_price = current_offer["price_of_kW"]
    current_renewable_percentage = current_offer["renewal_energy_percentage"]

    better_offers_related_to_price = [
        (company, data) for company, data in all_data.items()
        if (data["price_of_kW"] < current_price)
    ]
    better_offers_related_to_price.sort(key=lambda x: x[1]["price_of_kW"])

    better_offers_related_to_renewable_energy = [
        (company, data) for company, data in all_data.items()
        if (data["renewal_energy_percentage"] >= current_renewable_percentage)
    ]
    better_offers_related_to_renewable_energy.sort(key=lambda x: x[1]["renewal_energy_percentage"], reverse=True)

    better_offers = [offer for offer in better_offers_related_to_price if offer in better_offers_related_to_renewable_energy]

    return better_offers[:5]