"""
🦠 Module 1 – Crop Disease Detection & Organic Remedies
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import io
import streamlit as st
from PIL import Image

from config.settings import APP_ICON
from utils.gemini_utils import analyze_crop_disease
from utils.voice_utils import text_to_speech, is_voice_available

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Disease Detection", page_icon="🦠", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="farm-banner">
    <h1>🦠 Crop Disease Detection</h1>
    <p>Upload a photo of your crop — AI will identify the disease and suggest organic remedies</p>
</div>
""", unsafe_allow_html=True)

# ─── Tips ────────────────────────────────────────────────────────────────────
with st.expander("📸 Photo Tips for Best Results", expanded=False):
    st.markdown("""
    - 📷 Take a **close-up photo** of affected leaves/stems
    - 🌞 Use **natural light** — avoid flash
    - 🖼️ Ensure the disease/spot is **clearly visible**
    - 📐 Accepted formats: JPG, PNG, JPEG (max 10MB)
    """)

st.markdown("---")

# ─── Upload UI ───────────────────────────────────────────────────────────────
col_upload, col_preview = st.columns([1, 1])

with col_upload:
    st.markdown("### 📤 Upload Crop Image")
    uploaded_file = st.file_uploader(
        "Choose a crop image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear photo of your affected crop",
    )

    language = st.selectbox(
        "🔊 Voice Language",
        options=["en", "hi"],
        format_func=lambda x: "English" if x == "en" else "Hindi",
        index=0,
    )

    analyze_btn = st.button("🔍 Analyse Crop Disease", use_container_width=True, type="primary")

with col_preview:
    if uploaded_file:
        st.markdown("### 🖼️ Image Preview")
        img = Image.open(uploaded_file)
        st.image(img, use_column_width=True, caption=f"📸 {uploaded_file.name}")
        st.success(f"✅ Image loaded: {uploaded_file.name} ({uploaded_file.size // 1024} KB)")
    else:
        st.markdown("""
        <div style="background:#f9fbe7; border:2px dashed #A5D6A7; border-radius:12px;
                    padding:60px; text-align:center; color:#558B2F;">
            <div style="font-size:4rem">🌿</div>
            <p style="margin:10px 0 0; font-size:1rem;">Your crop image will appear here</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── Analysis ────────────────────────────────────────────────────────────────
if analyze_btn:
    if not uploaded_file:
        st.warning("⚠️ Please upload a crop image first.")
    else:
        with st.spinner("🔬 AI is analysing your crop... Please wait"):
            # Read image bytes
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()

            # Determine MIME type
            ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
            mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}
            mime_type = mime_map.get(ext, "image/jpeg")

            # Get AI analysis
            analysis = analyze_crop_disease(image_bytes, mime_type)

        st.markdown("## 🌿 AI Disease Analysis")
        st.markdown(analysis)

        # ─── Voice Output ─────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🎤 Listen to the Analysis")
        if is_voice_available():
            with st.spinner("🔊 Generating voice output..."):
                audio_bytes = text_to_speech(analysis, language=language)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
                st.caption("🎧 Press play to hear the farming advice")
            else:
                st.info("📢 Voice output could not be generated. Please read the text above.")
        else:
            st.info("📢 Voice feature requires gTTS library. Install with: `pip install gTTS`")

        # ─── Save to uploads ──────────────────────────────────────────────
        try:
            save_path = os.path.join("uploads", uploaded_file.name)
            os.makedirs("uploads", exist_ok=True)
            with open(save_path, "wb") as f:
                uploaded_file.seek(0)
                f.write(uploaded_file.read())
        except Exception:
            pass

        st.markdown("---")
        st.success("✅ Analysis complete! Follow the organic remedies above for best results.")
        st.info("💡 **Tip:** Apply Jeevamrut every 15 days to build crop immunity naturally.")

# ─── Sidebar info ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🦠 Disease Detection")
    st.markdown("""
    **How it works:**
    1. Upload crop photo
    2. AI analyses the image
    3. Get disease name + severity
    4. Receive organic treatment plan
    5. Listen to advice as audio 🎤
    """)
    st.markdown("---")
    st.markdown("**Powered by:** Google Gemini Vision AI")
    st.markdown("**Model:** gemini-1.5-flash")
