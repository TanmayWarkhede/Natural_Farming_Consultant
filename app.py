"""
🌱 Smart Voice-Based Natural Farming Consultant
Main entry point – run with: streamlit run app.py
"""
import os
import sys

# Ensure project root is on the path for clean imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from config.settings import APP_TITLE, APP_ICON
from database.init_db import init_database

# ─── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "Smart Natural Farming Consultant v1.0 – Powered by Gemini AI",
    },
)

# ─── Load CSS ─────────────────────────────────────────────────────────────────
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── One-time setup ──────────────────────────────────────────────────────────
os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)
init_database()

# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="farm-banner">
    <h1>🌱 Smart Natural Farming Consultant</h1>
    <p>AI-powered guidance for natural & organic farming — Disease detection, Weather intelligence & Market insights</p>
</div>
""", unsafe_allow_html=True)

# ─── Navigation cards ────────────────────────────────────────────────────────
st.markdown("### 🗺️ Navigate to a Module")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">🦠</div>
        <div class="value" style="font-size:1.1rem">Disease</div>
        <div class="label">Detect & Treat</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">🌦</div>
        <div class="value" style="font-size:1.1rem">Weather</div>
        <div class="label">Real-time Intel</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">📈</div>
        <div class="value" style="font-size:1.1rem">Market</div>
        <div class="label">Crop Prices</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">🤖</div>
        <div class="value" style="font-size:1.1rem">AI Chat</div>
        <div class="label">Farming Expert</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="stat-card">
        <div style="font-size:2.5rem">📊</div>
        <div class="value" style="font-size:1.1rem">Dashboard</div>
        <div class="label">Overview</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─── Quick start guide ───────────────────────────────────────────────────────
with st.expander("📖 How to use this app", expanded=False):
    st.markdown("""
    **Step 1 – Set your API key**  
    Add your Gemini API key to the `.env` file:  
    ```
    GEMINI_API_KEY=your_key_here
    ```
    Get a free key at [aistudio.google.com](https://aistudio.google.com)
    
    **Step 2 – Use the sidebar** to navigate between modules:
    - 🦠 **Disease Detection** – Upload a crop photo for AI diagnosis + organic remedies  
    - 🌦 **Weather Intelligence** – Get real-time weather + farming risk alerts  
    - 📈 **Market Intelligence** – View crop prices + AI selling strategy  
    - 🤖 **AI Assistant** – Chat with Krishi Mitra, your AI farming friend  
    - 📊 **Dashboard** – See all data at a glance  
    
    **Step 3 – Listen** 🎤 – Every AI response can be played as audio!
    """)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666; font-size:0.85rem;'>"
    "🌱 Natural Farming Consultant &nbsp;|&nbsp; Powered by Google Gemini AI &nbsp;|&nbsp; "
    "Weather by Open-Meteo (Free) &nbsp;|&nbsp; Voice by gTTS"
    "</div>",
    unsafe_allow_html=True,
)
