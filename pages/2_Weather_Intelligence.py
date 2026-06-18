"""
🌦 Module 2 – Weather Intelligence & Farming Risk Alerts
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from config.constants import INDIAN_CITIES
from utils.weather_utils import get_full_weather_data
from utils.gemini_utils import get_weather_farming_advice
from utils.voice_utils import text_to_speech, is_voice_available
from database.init_db import log_weather_query

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Weather Intelligence", page_icon="🌦", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="farm-banner">
    <h1>🌦 Weather Intelligence</h1>
    <p>Real-time weather data + AI farming risk analysis — powered by Open-Meteo (Free API)</p>
</div>
""", unsafe_allow_html=True)

# ─── Location input ──────────────────────────────────────────────────────────
col_input, col_voice = st.columns([3, 1])

with col_input:
    city_input = st.text_input(
        "📍 Enter your city / district name",
        placeholder="e.g. Pune, Nashik, Hyderabad, Lucknow...",
        value="Pune",
    )

with col_voice:
    language = st.selectbox(
        "🔊 Voice Language",
        options=["en", "hi"],
        format_func=lambda x: "English" if x == "en" else "Hindi",
    )

col_quick, _ = st.columns([3, 1])
with col_quick:
    st.caption("Quick select:")
    quick_cols = st.columns(5)
    quick_cities = ["Mumbai", "Delhi", "Nashik", "Jaipur", "Hyderabad"]
    for i, city in enumerate(quick_cities):
        if quick_cols[i].button(city, key=f"quick_{city}"):
            city_input = city

fetch_btn = st.button("🌤️ Get Weather & Farming Advice", use_container_width=True, type="primary")

st.markdown("---")

# ─── Fetch & Display ─────────────────────────────────────────────────────────
if fetch_btn or st.session_state.get("auto_fetch"):
    if not city_input.strip():
        st.warning("⚠️ Please enter a city name.")
    else:
        with st.spinner(f"🌐 Fetching live weather for {city_input}..."):
            weather = get_full_weather_data(city_input.strip())

        if "error" in weather:
            st.error(f"❌ Could not fetch weather: {weather['error']}")
            st.info("💡 Try a different city name or check your internet connection.")
        else:
            location = weather.get("location", city_input)
            st.success(f"✅ Live weather data for **{location}**")

            # ─── Metric cards ─────────────────────────────────────────────
            st.markdown("### 📊 Current Conditions")
            m1, m2, m3, m4 = st.columns(4)

            m1.metric(
                "🌡️ Temperature",
                f"{weather['temperature']}°C",
                f"Max {weather['temp_max']}° / Min {weather['temp_min']}°",
            )
            m2.metric("💧 Humidity", f"{weather['humidity']}%")
            m3.metric("🌧️ Rainfall Today", f"{weather['rainfall']} mm")
            m4.metric("💨 Wind Speed", f"{weather['wind_speed']} km/h")

            st.info(f"🌤️ **Condition:** {weather.get('condition', 'N/A')}")

            # ─── Risk alerts ──────────────────────────────────────────────
            st.markdown("### ⚠️ Farming Risk Alerts")
            risks = weather.get("risks", ["✅ No significant risks detected"])
            for risk in risks:
                if any(x in risk for x in ["HIGH", "🚫", "🦠", "🌡️", "💨"]):
                    st.markdown(f'<div class="risk-high">{risk}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="risk-ok">{risk}</div>', unsafe_allow_html=True)

            # ─── 3-day forecast ───────────────────────────────────────────
            forecast = weather.get("forecast", [])
            if forecast:
                st.markdown("### 📅 3-Day Forecast")
                fc_cols = st.columns(len(forecast))
                for i, day in enumerate(forecast):
                    with fc_cols[i]:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="label">{day.get('date', 'N/A')}</div>
                            <div class="value" style="font-size:1.4rem">
                                {day.get('temp_max', 0)}° / {day.get('temp_min', 0)}°
                            </div>
                            <div class="label">🌧️ {day.get('rain_mm', 0)} mm rain</div>
                        </div>
                        """, unsafe_allow_html=True)

            # ─── AI advice ────────────────────────────────────────────────
            st.markdown("---")
            st.markdown("### 🤖 AI Farming Recommendations")
            with st.spinner("🧠 Gemini AI is generating farming advice..."):
                advice = get_weather_farming_advice(weather)

            st.markdown(advice)

            # ─── Voice output ─────────────────────────────────────────────
            st.markdown("---")
            st.markdown("### 🎤 Listen to Farming Advice")
            if is_voice_available():
                with st.spinner("🔊 Converting to speech..."):
                    audio_bytes = text_to_speech(advice, language=language)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.caption("🎧 Press play to hear the weather-based farming advice")
                else:
                    st.info("📢 Voice output unavailable for this response.")
            else:
                st.info("📢 Install gTTS for voice: `pip install gTTS`")

            # ─── Log to DB ────────────────────────────────────────────────
            try:
                log_weather_query(
                    city=location,
                    temp=weather["temperature"],
                    humidity=weather["humidity"],
                    rainfall=weather["rainfall"],
                    risks="; ".join(weather.get("risks", [])),
                )
            except Exception:
                pass

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌦 Weather Intelligence")
    st.markdown("""
    **Data source:** Open-Meteo API  
    **Cost:** 100% Free, no API key  
    **Updates:** Real-time  
    
    **Risk Engine:**
    - 🌧️ Rain > 10mm → spray warning
    - 💧 Humidity > 80% → fungal risk
    - 🌡️ Temp > 38°C → irrigation alert
    - 💨 Wind > 30 km/h → spray delay
    """)
    st.markdown("---")
    st.markdown("**AI Advice by:** Google Gemini 1.5 Flash")
