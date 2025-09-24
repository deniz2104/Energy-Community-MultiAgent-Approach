from collections import defaultdict
import requests
import unicodedata
from HelperFiles.get_current_geolocation_via_api import get_location

def get_data():
    url = "https://posf.ro/api/v1/comparator?request=get-judete"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    return response.json()

def make_dictionaries_of_zones_and_cities():
    json_response = get_data()
    dictionary_of_zones_with_id = defaultdict()
    for data in json_response:
        zone_id = data["id_zona"]
        zone_name = data["nume"]
        dictionary_of_zones_with_id[zone_name] = zone_id
    return dictionary_of_zones_with_id

def get_zone_id_based_on_current_location():
    current_location = get_location()
    normalized_location = unicodedata.normalize('NFD', current_location).encode('ascii', 'ignore').decode('utf-8') if current_location else None

    if current_location is None:
        raise ValueError("Could not determine current location.")

    zones = list(make_dictionaries_of_zones_and_cities().keys())
    matching_zone = [zone for zone in zones if zone in normalized_location]
    return make_dictionaries_of_zones_and_cities().get(matching_zone[0])