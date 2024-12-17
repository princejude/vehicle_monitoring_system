import requests

API_KEY = "your_openweathermap_api_key"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"

def get_location(city_name):
    """
    Fetches the latitude and longitude for a given city name using OpenWeatherMap Geocoding API.

    :param city_name: Name of the city to fetch coordinates for.
    :return: A dictionary with latitude and longitude, or an error message.
    """
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        if data:
            location = {
                "latitude": data[0]["lat"],
                "longitude": data[0]["lon"]
            }
            return location
        else:
            return {"error": "City not found."}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    city = input("Enter the city name to fetch coordinates: ")
    location = get_location(city)
    if "error" in location:
        print(f"Error: {location['error']}")
    else:
        print(f"Latitude: {location['latitude']}, Longitude: {location['longitude']}")
