"""
Weather utilities using Open-Meteo API (no API key required).
"""
import requests
from typing import Optional

from config.settings import OPEN_METEO_BASE_URL, GEOCODING_BASE_URL
from config.constants import (
    RAIN_HIGH_THRESHOLD,
    HUMIDITY_HIGH_THRESHOLD,
    HEAT_HIGH_THRESHOLD,
    WIND_HIGH_THRESHOLD,
)

# WMO weather code descriptions
WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


def geocode_city(city_name: str) -> Optional[dict]:
    """Return lat/lon for a city name using Open-Meteo Geocoding API."""
    try:
        params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
        resp = requests.get(GEOCODING_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if results:
            r = results[0]
            return {
                "name": r.get("name", city_name),
                "country": r.get("country", ""),
                "latitude": r["latitude"],
                "longitude": r["longitude"],
            }
    except Exception:
        pass
    return None


def fetch_current_weather(latitude: float, longitude: float) -> Optional[dict]:
    """
    Fetch current weather + today's forecast from Open-Meteo.
    Returns a flat dict of weather values.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code",
            "precipitation",
        ],
        "daily": [
            "precipitation_sum",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "forecast_days": 3,
        "timezone": "Asia/Kolkata",
    }

    try:
        resp = requests.get(OPEN_METEO_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        daily = data.get("daily", {})

        temperature = current.get("temperature_2m", 0)
        humidity = current.get("relative_humidity_2m", 0)
        wind_speed = current.get("wind_speed_10m", 0)
        weather_code = current.get("weather_code", 0)
        precipitation = current.get("precipitation", 0)

        rainfall_today = (daily.get("precipitation_sum") or [0])[0]
        temp_max = (daily.get("temperature_2m_max") or [temperature])[0]
        temp_min = (daily.get("temperature_2m_min") or [temperature])[0]

        # Next 3 days forecast
        forecast = []
        dates = daily.get("time", [])
        rain_sums = daily.get("precipitation_sum") or []
        max_temps = daily.get("temperature_2m_max") or []
        min_temps = daily.get("temperature_2m_min") or []

        for i in range(min(3, len(dates))):
            forecast.append({
                "date": dates[i] if i < len(dates) else "N/A",
                "rain_mm": rain_sums[i] if i < len(rain_sums) else 0,
                "temp_max": max_temps[i] if i < len(max_temps) else 0,
                "temp_min": min_temps[i] if i < len(min_temps) else 0,
            })

        return {
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "wind_speed": round(wind_speed, 1),
            "weather_code": weather_code,
            "condition": WMO_CODES.get(weather_code, "Unknown"),
            "rainfall": round(rainfall_today, 1),
            "temp_max": round(temp_max, 1),
            "temp_min": round(temp_min, 1),
            "forecast": forecast,
        }

    except Exception as e:
        return {"error": str(e)}


def assess_farming_risks(weather: dict) -> list:
    """
    Simple rule-based risk engine.
    Returns list of risk strings.
    """
    risks = []

    temp = weather.get("temperature", 0)
    humidity = weather.get("humidity", 0)
    rainfall = weather.get("rainfall", 0)
    wind = weather.get("wind_speed", 0)

    if rainfall >= RAIN_HIGH_THRESHOLD:
        risks.append(f"🚫 HIGH RAINFALL ({rainfall}mm) – Avoid spraying today")
    if humidity >= HUMIDITY_HIGH_THRESHOLD:
        risks.append(f"🦠 HIGH HUMIDITY ({humidity}%) – Fungal disease risk; inspect crops")
    if temp >= HEAT_HIGH_THRESHOLD:
        risks.append(f"🌡️ HIGH HEAT ({temp}°C) – Irrigate early morning or evening")
    if wind >= WIND_HIGH_THRESHOLD:
        risks.append(f"💨 HIGH WIND ({wind} km/h) – Delay spray applications")

    if not risks:
        risks.append("✅ Conditions are suitable for normal farming activities")

    return risks


def get_full_weather_data(city_name: str) -> dict:
    """
    Orchestrator: geocode → fetch weather → assess risks.
    Returns a unified dict safe to pass to UI and Gemini.
    """
    geo = geocode_city(city_name)
    if not geo:
        return {
            "error": f"Could not find location: {city_name}",
            "location": city_name,
        }

    weather = fetch_current_weather(geo["latitude"], geo["longitude"])
    if not weather or "error" in weather:
        return {
            "error": weather.get("error", "Unknown error fetching weather"),
            "location": f"{geo['name']}, {geo['country']}",
        }

    risks = assess_farming_risks(weather)
    weather["location"] = f"{geo['name']}, {geo['country']}"
    weather["risks"] = risks
    weather["latitude"] = geo["latitude"]
    weather["longitude"] = geo["longitude"]
    return weather
