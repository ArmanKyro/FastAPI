from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

OPENWEATHER_API_KEY = ""
IQAIR_API_KEY = ""

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
