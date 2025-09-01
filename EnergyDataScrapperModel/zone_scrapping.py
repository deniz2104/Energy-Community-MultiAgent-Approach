from collections import defaultdict
import requests

def get_data():
    url = "https://posf.ro/api/v1/comparator?request=get-judete"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    return response.json()

def make_dictionaries_of_zones_and_cities():
    json_response = get_data()
    dictionary_of_zones_with_id = defaultdict(list)
    for data in json_response:
        zone_id = data["id_zona"]
        zone_name = data["nume"]
        dictionary_of_zones_with_id[zone_id].append(zone_name)
    return dictionary_of_zones_with_id