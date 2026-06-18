import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.5-flash"

# Open-Meteo API (no key needed)
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

# App settings
APP_TITLE = "🌱 Smart Natural Farming Consultant"
APP_ICON = "🌱"
UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"
DATA_FOLDER = "data"
