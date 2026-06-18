"""
📊 Module 5 – Overview Dashboard
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd

from utils.market_utils import load_crop_prices, compute_market_summary, get_category_stats
from utils.weather_utils import get_full_weather_data
from utils.voice_utils import is_voice_available
from config.settings import GEMINI_API_KEY

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="farm-banner">
    <h1>📊 Farming Dashboard</h1>
    <p>Your complete natural farming overview — all insights in one place</p>
</div>
""", unsafe_allow_html=True)

# ─── System status ────────────────────────────────────────────────────────────
st.markdown("### ⚙️ System Status")
s1, s2, s3, s4 = st.columns(4)

api_ok = bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here")
df = load_crop_prices()
market_ok = df is not None and not df.empty
voice_ok = is_voice_available()

with s1:
    icon = "✅" if api_ok else "⚠️"
    color = "#2E7D32" if api_ok else "#F57F17"
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size:2rem">{icon}</div>
        <div class="value" style="font-size:1rem; color:{color}">Gemini AI</div>
        <div class="label">{"Connected" if api_ok else "API key missing"}</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2rem">✅</div>
        <div class="value" style="font-size:1rem; color:#2E7D32">Weather API</div>
        <div class="label">Open-Meteo (Free)</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    icon = "✅" if market_ok else "⚠️"
    color = "#2E7D32" if market_ok else "#F57F17"
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size:2rem">{icon}</div>
        <div class="value" style="font-size:1rem; color:{color}">Market Data</div>
        <div class="label">{"CSV loaded" if market_ok else "CSV missing"}</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    icon = "✅" if voice_ok else "⚠️"
    color = "#2E7D32" if voice_ok else "#F57F17"
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size:2rem">{icon}</div>
        <div class="value" style="font-size:1rem; color:{color}">Voice (gTTS)</div>
        <div class="label">{"Available" if voice_ok else "Install gTTS"}</div>
    </div>
    """, unsafe_allow_html=True)

if not api_ok:
    st.warning(
        "⚠️ **Gemini API key not set.** Add `GEMINI_API_KEY=your_key` to the `.env` file. "
        "Get a free key at [aistudio.google.com](https://aistudio.google.com)"
    )

st.markdown("---")

# ─── Market snapshot ──────────────────────────────────────────────────────────
st.markdown("### 📈 Market Snapshot")

if market_ok:
    summary = compute_market_summary(df)
    c1, c2, c3 = st.columns(3)

    c1.metric("🏆 Top Earner", summary.get("highest_crop", "N/A"),
              f"₹{summary.get('highest_price', 0):,.0f}/qtl")
    c2.metric("📦 Total Crops", summary.get("total_crops", 0))
    c3.metric("📊 Avg Market Price", f"₹{summary.get('avg_price', 0):,.0f}/qtl")

    # Category bar data
    cat_stats = get_category_stats(df)
    if cat_stats is not None:
        st.markdown("#### Price by Category")
        # Display as a simple styled table with visual bars
        max_price = cat_stats["avg_price"].max()
        for _, row in cat_stats.iterrows():
            pct = int((row["avg_price"] / max_price) * 100)
            st.markdown(f"""
            <div style="margin:6px 0;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:160px; font-size:0.9rem; color:#333;">{row['category']}</div>
                    <div style="flex:1; background:#E8F5E9; border-radius:20px; height:22px; overflow:hidden;">
                        <div style="width:{pct}%; background:linear-gradient(90deg,#2E7D32,#66BB6A);
                                    height:100%; border-radius:20px;"></div>
                    </div>
                    <div style="width:110px; text-align:right; font-weight:700; color:#2E7D32;">
                        ₹{row['avg_price']:,.0f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("📁 Market data unavailable. Add `data/crop_prices.csv` to enable this section.")

st.markdown("---")

# ─── Quick weather check ──────────────────────────────────────────────────────
st.markdown("### 🌦 Quick Weather Check")
col_city, col_btn = st.columns([4, 1])
with col_city:
    dash_city = st.text_input("📍 City for quick weather", value="Pune", label_visibility="collapsed")
with col_btn:
    weather_btn = st.button("🌤️ Check", use_container_width=True)

if weather_btn and dash_city:
    with st.spinner(f"Fetching weather for {dash_city}..."):
        w = get_full_weather_data(dash_city.strip())

    if "error" not in w:
        wc1, wc2, wc3, wc4 = st.columns(4)
        wc1.metric("🌡️ Temp", f"{w.get('temperature', 'N/A')}°C")
        wc2.metric("💧 Humidity", f"{w.get('humidity', 'N/A')}%")
        wc3.metric("🌧️ Rainfall", f"{w.get('rainfall', 'N/A')} mm")
        wc4.metric("💨 Wind", f"{w.get('wind_speed', 'N/A')} km/h")
        st.info(f"🌤️ {w.get('condition', '')} | {w.get('location', dash_city)}")
        for risk in w.get("risks", []):
            if "✅" in risk:
                st.success(risk)
            else:
                st.warning(risk)
    else:
        st.error(f"Could not fetch weather: {w['error']}")

st.markdown("---")

# ─── Module navigator ─────────────────────────────────────────────────────────
st.markdown("### 🗺️ Jump to a Module")
nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">🦠</div>
        <div class="value" style="font-size:1rem">Disease Detection</div>
        <div class="label">Upload crop photo → AI diagnosis + organic remedies</div>
    </div>
    """, unsafe_allow_html=True)

with nav2:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">🌦</div>
        <div class="value" style="font-size:1rem">Weather Intel</div>
        <div class="label">Real-time weather + farming risk alerts</div>
    </div>
    """, unsafe_allow_html=True)

with nav3:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">📈</div>
        <div class="value" style="font-size:1rem">Market Intelligence</div>
        <div class="label">Crop prices + AI selling strategy</div>
    </div>
    """, unsafe_allow_html=True)

with nav4:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">🤖</div>
        <div class="value" style="font-size:1rem">AI Assistant</div>
        <div class="label">Chat with Krishi Mitra anytime</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Natural farming tips carousel ───────────────────────────────────────────
st.markdown("---")
st.markdown("### 🌱 Daily Natural Farming Tip")

tips = [
    ("🐄 Jeevamrut", "Mix 10L cow dung, 10L cow urine, 2kg jaggery, 2kg gram flour, 1 handful soil in 200L water. Ferment 48 hours. Apply 200L/acre every 15 days."),
    ("🌿 Neem Spray", "Soak 5kg neem leaves in 20L water overnight. Filter and dilute to 200L. Spray on leaves early morning to repel pests organically."),
    ("🌍 Mulching", "Cover soil with dry leaves, straw, or crop residue. Retains moisture, suppresses weeds, improves soil biology — no cost!"),
    ("🌱 Bijamrut", "Treat seeds with Bijamrut (cow dung + cow urine + lime + soil solution) before sowing. Protects from soil-borne diseases naturally."),
    ("🔄 Crop Rotation", "Never grow the same crop in the same field twice in a row. Rotate between cereals, pulses, and vegetables to maintain soil health."),
    ("🌸 Companion Planting", "Plant marigold, basil, or coriander near vegetables. They repel pests naturally and attract beneficial insects like bees."),
]

import datetime
tip_idx = datetime.datetime.now().day % len(tips)
tip_title, tip_content = tips[tip_idx]

st.markdown(f"""
<div style="background:linear-gradient(135deg,#E8F5E9,#F1F8E9); border-radius:14px;
            padding:20px 24px; border-left:5px solid #2E7D32;">
    <h4 style="color:#1B5E20; margin:0 0 8px;">{tip_title}</h4>
    <p style="color:#388E3C; margin:0; line-height:1.6;">{tip_content}</p>
</div>
""", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.8rem;'>"
    "🌱 Natural Farming Consultant &nbsp;|&nbsp; Built with Streamlit + Gemini AI + Open-Meteo"
    "</div>",
    unsafe_allow_html=True,
)
