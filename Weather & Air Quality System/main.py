# from fastapi import FastAPI, HTTPException
# import requests

# app = FastAPI()

# OPENWEATHER_API_KEY = ""
# IQAIR_API_KEY = ""

# ############################################### GET-COORDINATES ######################################################

# @app.get("/")
# def get_city_coordinates(city: str):
#     """Fetch latitude & longitude for a city using OpenStreetMap Nominatim API."""
#     geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
#     headers = {"User-Agent": "FastAPI-App"}  # Required to prevent request blocking
#     response = requests.get(geo_url, headers=headers)

#     if response.status_code != 200 or not response.json():
#         raise HTTPException(status_code=404, detail="City not found")

#     data = response.json()[0]  # First search result
#     return {"city": city, "latitude": float(data["lat"]), "longitude": float(data["lon"])}

# ############################################### GET WEATHER ######################################################

# @app.get("/weather")
# def get_weather(city: str):
#     """Fetch current weather data using OpenWeather API (Free Tier)."""
#     weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
#     response = requests.get(weather_url)
    
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Weather data not available")
    
#     data = response.json()
#     return {
#         "city": city,
#         "temperature": data["main"]["temp"],
#         "humidity": data["main"]["humidity"],
#         "weather": data["weather"][0]["description"],
#         "wind_speed": data["wind"]["speed"]
#     }

# ############################################### AIR-QUALITY ######################################################


# IQAIR_API_KEY = "8a2b633c-4e17-40a7-8a7e-654a72edd49c"

# def get_air_quality(city: str, state: str, country: str):
#     """Fetch real-time air quality data using the IQAir API."""
#     air_quality_url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={IQAIR_API_KEY}"

#     response = requests.get(air_quality_url)

#     if response.status_code != 200 or response.json().get("status") != "success":
#         print("Air Quality API Response:", response.status_code, response.text)  # Debugging Output
#         raise HTTPException(status_code=400, detail=f"Air quality data not available: {response.text}")

#     data = response.json()["data"]
#     return {
#         "city": city,
#         "state": state,
#         "country": country,
#         "AQI": data["current"]["pollution"]["aqius"],  # AQI (US standard)
#         "pollution_level": "Good" if data["current"]["pollution"]["aqius"] <= 50 else "Unhealthy",
#         "temperature": data["current"]["weather"]["tp"],  # Temperature in °C
#         "humidity": data["current"]["weather"]["hu"],  # Humidity %
#         "wind_speed": data["current"]["weather"]["ws"]  # Wind speed (m/s)
#     }

# @app.get("/air-quality")
# def get_air_quality_by_city(city: str, state: str, country: str):
#     """API to get air quality by city, state, and country."""
#     air_quality = get_air_quality(city, state, country)
#     return air_quality




from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

OPENWEATHER_API_KEY = "f6bdb85a6087a5ee3dc840e6db5c3f40"
IQAIR_API_KEY = "8a2b633c-4e17-40a7-8a7e-654a72edd49c"

############################################### GET WEATHER ######################################################

def fetch_weather(city: str):
    """Fetch current weather data from OpenWeather API."""
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(weather_url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Weather data not available")
    
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

############################################### GET AIR QUALITY ##################################################

def fetch_air_quality(city: str, state: str, country: str):
    """Fetch air quality data from IQAir API."""
    air_quality_url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={IQAIR_API_KEY}"
    response = requests.get(air_quality_url)

    if response.status_code != 200 or response.json().get("status") != "success":
        raise HTTPException(status_code=400, detail="Air quality data not available")

    data = response.json()["data"]
    return {
        "AQI": data["current"]["pollution"]["aqius"],
        "pollution_level": "Good" if data["current"]["pollution"]["aqius"] <= 50 else "Unhealthy",
        "temperature": data["current"]["weather"]["tp"],
        "humidity": data["current"]["weather"]["hu"],
        "wind_speed": data["current"]["weather"]["ws"]
    }

############################################### COMBINED API CALL ##################################################

@app.get("/combined-weather-airquality")
def get_combined_data(city: str, state: str, country: str):
    """API to fetch weather and air quality in a single call."""
    weather_data = fetch_weather(city)
    air_quality_data = fetch_air_quality(city, state, country)

    return {
        "city": city,
        "weather": weather_data,
        "air_quality": air_quality_data
    }
