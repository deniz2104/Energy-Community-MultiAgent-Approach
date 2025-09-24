import requests

def get_location():
    url = "http://ip-api.com/json/"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "success":
        return data["regionName"]
    else:
        return None