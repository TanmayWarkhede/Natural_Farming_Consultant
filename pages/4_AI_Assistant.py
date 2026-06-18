"""
🤖 Module 4 – Krishi Mitra AI Farming Assistant (Multi-turn Chat)
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from utils.gemini_utils import chat_with_assistant
from utils.voice_utils import text_to_speech, is_voice_available

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="farm-banner">
    <h1>🤖 Krishi Mitra – AI Farming Assistant</h1>
    <p>Your personal natural farming expert — ask anything about crops, pests, soil, and organic methods</p>
</div>
""", unsafe_allow_html=True)

# ─── Session state initialisation ────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []          # [{role, content}] for display
if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = []        # [{role, parts}] for Gemini API

# ─── Sidebar controls ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 Krishi Mitra")
    language = st.selectbox(
        "🔊 Voice Language",
        options=["en", "hi"],
        format_func=lambda x: "English" if x == "en" else "Hindi",
    )
    voice_enabled = st.checkbox("🎤 Auto voice for responses", value=False)

    st.markdown("---")
    st.markdown("**Suggested Questions:**")
    suggestions = [
        "How to make Jeevamrut at home?",
        "What is Panchagavya and how to use it?",
        "How to control aphids organically?",
        "Best crops for summer in Maharashtra?",
        "How to improve soil fertility naturally?",
        "What is Zero Budget Natural Farming?",
        "How to make neem spray for pests?",
        "When to apply Bijamrut for seeds?",
    ]
    for q in suggestions:
        if st.button(q, key=f"sugg_{q[:20]}"):
            st.session_state["prefill_question"] = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.gemini_history = []
        st.rerun()

    st.markdown("**Powered by:** Gemini 1.5 Flash")

# ─── Chat display ─────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="background:#E8F5E9; border-radius:14px; padding:24px; text-align:center;
                    border: 1px solid #A5D6A7; margin-bottom:20px;">
            <div style="font-size:3rem">🌱</div>
            <h3 style="color:#2E7D32; margin:8px 0;">Namaste! I'm Krishi Mitra</h3>
            <p style="color:#558B2F; margin:0;">
                Your AI farming friend specialising in natural & organic farming.<br>
                Ask me anything about crops, pests, soil health, Jeevamrut, and more!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                with st.chat_message("user", avatar="👨‍🌾"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant", avatar="🌱"):
                    st.markdown(content)
                    # Show audio inline if voice was generated
                    if "audio" in msg and msg["audio"]:
                        st.audio(msg["audio"], format="audio/mp3")

# ─── Chat input ───────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill_question", "")
user_input = st.chat_input(
    "Ask Krishi Mitra anything about natural farming...",
    key="chat_input",
)

# Handle prefill from sidebar suggestion buttons
if prefill and not user_input:
    user_input = prefill

if user_input:
    # Add user message to display history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Show user message immediately
    with st.chat_message("user", avatar="👨‍🌾"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant", avatar="🌱"):
        with st.spinner("🌿 Krishi Mitra is thinking..."):
            response = chat_with_assistant(
                messages=st.session_state.gemini_history,
                user_input=user_input,
            )

        st.markdown(response)

        # Voice output
        audio_bytes = None
        if voice_enabled and is_voice_available():
            with st.spinner("🔊 Generating voice..."):
                audio_bytes = text_to_speech(response, language=language)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
        elif not voice_enabled:
            # Show a one-click voice button
            if is_voice_available():
                if st.button("🔊 Play this response", key=f"play_{len(st.session_state.chat_history)}"):
                    with st.spinner("🔊 Generating voice..."):
                        audio_bytes = text_to_speech(response, language=language)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")

    # Update histories
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "audio": audio_bytes,
    })

    # Update Gemini history (role must be "user" or "model")
    st.session_state.gemini_history.append(
        {"role": "user", "parts": [user_input]}
    )
    st.session_state.gemini_history.append(
        {"role": "model", "parts": [response]}
    )

    # Keep history manageable (last 10 exchanges = 20 messages)
    if len(st.session_state.gemini_history) > 20:
        st.session_state.gemini_history = st.session_state.gemini_history[-20:]
