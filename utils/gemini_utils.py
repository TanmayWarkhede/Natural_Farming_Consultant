"""
Gemini AI utility – wraps all calls to google-generativeai.
No circular imports: this module imports only from stdlib / third-party.
"""
import io
import base64
from typing import Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from config.constants import (
    FALLBACK_DISEASE_RESPONSE,
    FALLBACK_WEATHER_RESPONSE,
    FALLBACK_MARKET_RESPONSE,
)


def _get_model():
    """Initialise and return a Gemini GenerativeModel, or None on failure."""
    if not GENAI_AVAILABLE:
        return None
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel(GEMINI_MODEL)
    except Exception:
        return None


def analyze_crop_disease(image_bytes: bytes, image_mime: str = "image/jpeg") -> str:
    """
    Send a crop image to Gemini Vision and return organic-farming advice.
    Falls back gracefully if the API is unavailable.
    """
    model = _get_model()
    if model is None:
        return FALLBACK_DISEASE_RESPONSE

    prompt = """
You are an expert organic farming advisor who speaks like a helpful village agronomist.

Carefully examine this crop image and provide:

1. 🌾 **Crop Identified**: Name of the crop
2. 🦠 **Disease / Problem**: What disease, pest, or deficiency you see
3. 🔴 **Severity**: Low / Medium / High
4. 📋 **Symptoms**: What visible signs you observed

Then provide ONLY NATURAL / ORGANIC remedies:

5. 🌿 **Neem-Based Treatment**: Specific neem spray recipe and schedule
6. 🐄 **Jeevamrut Recommendation**: How to prepare and apply Jeevamrut
7. 🌱 **Other Organic Remedies**: Additional natural treatments (garlic spray, turmeric, ash, etc.)
8. 🛡️ **Prevention Steps**: How to avoid this problem in future
9. 💬 **Simple Farmer Explanation**: Explain the problem and solution in very simple words a farmer can understand

Keep the language friendly, practical, and encouraging. Avoid chemical pesticide recommendations.
"""

    try:
        image_part = {"mime_type": image_mime, "data": image_bytes}
        response = model.generate_content([prompt, image_part])
        return response.text if response.text else FALLBACK_DISEASE_RESPONSE
    except Exception as e:
        return f"{FALLBACK_DISEASE_RESPONSE}\n\n*(API note: {str(e)[:120]})*"


def get_weather_farming_advice(weather_summary: dict) -> str:
    """
    Pass structured weather data to Gemini and get farming recommendations.
    """
    model = _get_model()
    if model is None:
        return FALLBACK_WEATHER_RESPONSE

    prompt = f"""
You are a smart farming advisor helping small-scale Indian farmers.

Current weather conditions:
- Location: {weather_summary.get('location', 'Unknown')}
- Temperature: {weather_summary.get('temperature', 'N/A')}°C
- Humidity: {weather_summary.get('humidity', 'N/A')}%
- Rainfall (today): {weather_summary.get('rainfall', 'N/A')} mm
- Wind Speed: {weather_summary.get('wind_speed', 'N/A')} km/h
- Weather Code Description: {weather_summary.get('condition', 'N/A')}
- Risk Flags: {', '.join(weather_summary.get('risks', ['None']))}

Based on this weather data, give practical farming advice:

1. 🌾 **Today's Farming Tasks**: What should the farmer do today?
2. 💧 **Irrigation Advice**: Should they water crops today or not?
3. 🚫 **Spray Warning**: Is it safe to spray pesticides/fertilisers today?
4. 🦠 **Disease Risk**: Any fungal or pest risk based on weather?
5. 🌱 **Crop Protection**: Steps to protect crops from this weather
6. 📅 **Next 3 Days Tip**: Brief advice for the coming days

Use simple Hindi-English mixed language if possible. Be specific and actionable.
"""

    try:
        response = model.generate_content(prompt)
        return response.text if response.text else FALLBACK_WEATHER_RESPONSE
    except Exception as e:
        return f"{FALLBACK_WEATHER_RESPONSE}\n\n*(API note: {str(e)[:120]})*"


def get_market_selling_advice(market_summary: dict) -> str:
    """
    Generate AI selling strategy from crop price data.
    """
    model = _get_model()
    if model is None:
        return FALLBACK_MARKET_RESPONSE

    prompt = f"""
You are an agricultural market expert helping farmers get the best price for their produce.

Current market data:
- Total crops tracked: {market_summary.get('total_crops', 0)}
- Highest priced crop: {market_summary.get('highest_crop', 'N/A')} at ₹{market_summary.get('highest_price', 0)}/quintal
- Lowest priced crop: {market_summary.get('lowest_crop', 'N/A')} at ₹{market_summary.get('lowest_price', 0)}/quintal
- Average market price: ₹{market_summary.get('avg_price', 0)}/quintal
- Top 3 earners: {market_summary.get('top_crops', [])}

Provide actionable market intelligence:

1. 💰 **Best Crops to Sell Now**: Which crops should the farmer prioritise selling?
2. 📦 **Storage Advice**: Which crops to store and wait for better prices?
3. 🤝 **Negotiation Tips**: How to get a better price at the mandi?
4. 🌿 **Organic Premium**: How to position produce as organic for better returns?
5. 📱 **Direct Selling**: Ideas for bypassing middlemen (apps, cooperatives, etc.)
6. ⚠️ **Market Warning**: Any crops to be cautious about?

Use simple, practical language. Give specific rupee estimates where possible.
"""

    try:
        response = model.generate_content(prompt)
        return response.text if response.text else FALLBACK_MARKET_RESPONSE
    except Exception as e:
        return f"{FALLBACK_MARKET_RESPONSE}\n\n*(API note: {str(e)[:120]})*"


def chat_with_assistant(messages: list, user_input: str) -> str:
    """
    Multi-turn AI farming assistant chat.
    messages: list of {"role": "user"/"model", "parts": [text]} dicts
    """
    model = _get_model()
    if model is None:
        return (
            "🌱 I'm your farming assistant! Currently running in offline mode "
            "because the AI service is unavailable. Please check your API key in the .env file.\n\n"
            "**General advice:** Follow natural farming principles – use Jeevamrut, "
            "neem spray, and compost for healthy crops."
        )

    system_context = """
You are Krishi Mitra (Farm Friend), a smart natural farming assistant for Indian farmers.

Your personality:
- Speak in simple, friendly language (Hindi-English mix welcome)
- Always recommend natural/organic methods first
- Be encouraging and positive
- Give specific, actionable advice
- Reference traditional Indian farming wisdom when relevant
- Never recommend synthetic pesticides or chemical fertilisers

You specialise in:
- Natural farming techniques (Zero Budget Natural Farming - ZBNF)
- Jeevamrut, Bijamrut, Panchagavya preparation
- Organic pest management
- Crop rotation and companion planting
- Soil health improvement
- Water conservation
"""

    try:
        chat = model.start_chat(history=messages)
        full_prompt = system_context + "\n\nFarmer asks: " + user_input
        response = chat.send_message(full_prompt)
        return response.text if response.text else "I couldn't generate a response. Please try again."
    except Exception as e:
        return f"🌱 Sorry, I'm having trouble connecting right now. Please try again in a moment.\n*(Error: {str(e)[:100]})*"
