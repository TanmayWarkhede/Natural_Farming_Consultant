"""
📈 Module 3 – Market Intelligence & Crop Price Analysis
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd

from utils.market_utils import (
    load_crop_prices,
    compute_market_summary,
    get_category_stats,
    filter_by_category,
)
from utils.gemini_utils import get_market_selling_advice
from utils.voice_utils import text_to_speech, is_voice_available

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Market Intelligence", page_icon="📈", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="farm-banner">
    <h1>📈 Market Intelligence</h1>
    <p>Live crop prices, market trends & AI-powered selling strategy</p>
</div>
""", unsafe_allow_html=True)

# ─── Load data ───────────────────────────────────────────────────────────────
df = load_crop_prices()

if df is None or df.empty:
    st.error("❌ Could not load crop price data. Please ensure `data/crop_prices.csv` exists.")
    st.info("📁 Expected file: `data/crop_prices.csv` with columns: crop, price_per_quintal, category")
    st.stop()

# ─── Summary metrics ─────────────────────────────────────────────────────────
summary = compute_market_summary(df)

st.markdown("### 💰 Market Summary")
m1, m2, m3, m4 = st.columns(4)

m1.metric("📦 Total Crops Tracked", summary.get("total_crops", 0))
m2.metric(
    "🏆 Highest Price",
    f"₹{summary.get('highest_price', 0):,.0f}/qtl",
    summary.get("highest_crop", ""),
)
m3.metric(
    "📉 Lowest Price",
    f"₹{summary.get('lowest_price', 0):,.0f}/qtl",
    summary.get("lowest_crop", ""),
)
m4.metric("📊 Average Price", f"₹{summary.get('avg_price', 0):,.0f}/qtl")

st.markdown("---")

# ─── Filter controls ─────────────────────────────────────────────────────────
col_filter, col_sort, col_voice = st.columns([2, 2, 1])

categories = ["All"] + sorted(df["category"].dropna().unique().tolist())

with col_filter:
    selected_cat = st.selectbox("🗂️ Filter by Category", options=categories)

with col_sort:
    sort_order = st.selectbox(
        "↕️ Sort by Price",
        options=["Highest First", "Lowest First", "Alphabetical"],
    )

with col_voice:
    language = st.selectbox(
        "🔊 Voice",
        options=["en", "hi"],
        format_func=lambda x: "English" if x == "en" else "Hindi",
    )

# ─── Filter & sort dataframe ──────────────────────────────────────────────────
filtered_df = filter_by_category(df, selected_cat)

if sort_order == "Highest First":
    filtered_df = filtered_df.sort_values("price_per_quintal", ascending=False)
elif sort_order == "Lowest First":
    filtered_df = filtered_df.sort_values("price_per_quintal", ascending=True)
else:
    filtered_df = filtered_df.sort_values("crop", ascending=True)

# ─── Price table ─────────────────────────────────────────────────────────────
st.markdown(f"### 🌾 Crop Prices — {selected_cat} ({len(filtered_df)} crops)")

display_df = filtered_df[["crop", "category", "price_per_quintal", "market", "state"]].copy()
display_df.columns = ["Crop", "Category", "Price (₹/Quintal)", "Market", "State"]
display_df["Price (₹/Quintal)"] = display_df["Price (₹/Quintal)"].apply(
    lambda x: f"₹{x:,.0f}"
)

st.dataframe(display_df, use_container_width=True, hide_index=True)

# ─── Category averages ───────────────────────────────────────────────────────
cat_stats = get_category_stats(df)
if cat_stats is not None:
    st.markdown("### 📊 Average Price by Category")
    cat_display = cat_stats.copy()
    cat_display.columns = ["Category", "Avg Price (₹/Quintal)"]
    cat_display["Avg Price (₹/Quintal)"] = cat_display["Avg Price (₹/Quintal)"].apply(
        lambda x: f"₹{x:,.0f}"
    )
    st.dataframe(cat_display, use_container_width=True, hide_index=True)

# ─── Top earners ─────────────────────────────────────────────────────────────
st.markdown("### 🏅 Top 5 Highest-Value Crops")
top5 = df.nlargest(5, "price_per_quintal")[["crop", "price_per_quintal", "category"]]
top5_cols = st.columns(5)
for i, (_, row) in enumerate(top5.iterrows()):
    with top5_cols[i]:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size:1.8rem">🌾</div>
            <div class="value" style="font-size:1rem">{row['crop']}</div>
            <div class="value" style="font-size:1.3rem; color:#1B5E20">
                ₹{row['price_per_quintal']:,.0f}
            </div>
            <div class="label">{row['category']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── AI selling advice ───────────────────────────────────────────────────────
st.markdown("### 🤖 AI Selling Strategy")
advice_btn = st.button("💡 Get AI Market Advice", use_container_width=True, type="primary")

if advice_btn:
    with st.spinner("🧠 Gemini AI is analysing market data..."):
        top_crops_list = [
            f"{r['crop']} (₹{r['price_per_quintal']}/qtl)"
            for r in summary.get("top_crops", [])
        ]
        advice = get_market_selling_advice({**summary, "top_crops": top_crops_list})

    st.markdown(advice)

    # ─── Voice output ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎤 Listen to Market Advice")
    if is_voice_available():
        with st.spinner("🔊 Converting to speech..."):
            audio_bytes = text_to_speech(advice, language=language)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.caption("🎧 Press play to hear the market selling strategy")
        else:
            st.info("📢 Voice output unavailable for this response.")
    else:
        st.info("📢 Install gTTS for voice: `pip install gTTS`")

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📈 Market Intelligence")
    st.markdown("""
    **Data:** crop_prices.csv (APMC rates)  
    **Categories tracked:**
    - 🥦 Vegetables
    - 🍎 Fruits
    - 🌾 Grains & Cereals
    - 🫘 Pulses & Legumes
    - 🌶️ Spices
    - 🌿 Cash Crops
    """)
    st.markdown("---")
    st.markdown("**AI Strategy by:** Google Gemini 1.5 Flash")
    st.markdown("""
    💡 **Tip:** Organic produce commands  
    20–30% premium at most mandis!
    """)
