import requests

def get_location(url: str = "http://ip-api.com/json/") -> str | None:
    response = requests.get(url)
    data = response.json()
    return data.get("regionName") if response.status_code == 200 else None