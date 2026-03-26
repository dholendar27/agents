import os

import googlemaps
import requests
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("GOOGLE_MAPS_KEY"):
    print("Please Enter google Maps Key")
    exit()


gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_KEY"))


def get_climate_details(lattitude: str, longitude: str):
    try:
        weather_data = requests.get(
            f"https://weather.googleapis.com/v1/forecast/days:lookup?key={os.getenv('GOOGLE_MAPS_KEY')}&location.latitude={lattitude}&location.longitude={longitude}&days=7"
        )
        if weather_data.status_code == 200:
            return weather_data.json()
        return "Error Retrieveing the weather"
    except Exception as e:
        print(str(e))


def get_lat_lng(city_name: str):
    geocode_results = gmaps.geocode(city_name)
    lat_lng = geocode_results[0]["geometry"]["location"]
    return lat_lng


def fetch_weather_by_location(location: str):
    lat_lng = get_lat_lng("Bangalore")
    return get_climate_details(lattitude=lat_lng["lat"], longitude=lat_lng["lng"])


if __name__ == "__main__":
    lat_lng = get_lat_lng("Bangalore")
    get_climate_details(lattitude=lat_lng["lat"], longitude=lat_lng["lng"])
