import requests

def get_aircraft_position(icao):
    url = f"https://opensky-network.org/api/states/all?icao24={icao}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None
