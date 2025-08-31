import requests

url = "https://posf.ro/api/v1/comparator?request=get-judete"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
json_response = response.json()
dictionary_of_zones_with_id :dict[str,list[str]] = {}
for data in json_response:
    dictionary_of_zones_with_id[data["id_zona"]] = dictionary_of_zones_with_id.get(data["id_zona"], []) + [data["nume"]]
dictionary_of_zones_with_id = dict(sorted(dictionary_of_zones_with_id.items(), key=lambda x: int(x[0])))
