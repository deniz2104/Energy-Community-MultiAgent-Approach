import requests
import datetime
from EnergyDataScrapperModel.get_parameters_for_scrapper import GetTypeOffer,GetTypeProduct

def set_params():
    params = {
    "request": "comparator-electric",
    "tip_oferta": GetTypeOffer.ORICARE.value,
    "data_start_aplicare": datetime.datetime.now().strftime("%Y-%m-%d"),
    "tip_client": "casnic",
    "tip_pret": "nediferentiat",
    "nivel_tensiune": "JT_",
    "id_zona": "6",
    "tip_produs": GetTypeProduct.ORICARE.value
    }
    return params

def get_data():
    url = "https://posf.ro/api/v1/comparator"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}, params=set_params())
    return response.json()