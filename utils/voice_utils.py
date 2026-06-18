"""
Voice utilities – converts text to speech using gTTS.
Returns audio bytes that Streamlit can play with st.audio().
"""
import io
import re
from typing import Optional

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


def clean_text_for_speech(text: str) -> str:
    """
    Strip markdown symbols so gTTS reads clean speech.
    """
    # Remove markdown bold/italic
    text = re.sub(r"\*{1,3}(.*?)\*{1,3}", r"\1", text)
    # Remove headers
    text = re.sub(r"#{1,6}\s*", "", text)
    # Remove emojis (basic ranges)
    text = re.sub(
        r"[\U00010000-\U0010ffff\U0001F300-\U0001F9FF\u2600-\u27BF]",
        "",
        text,
        flags=re.UNICODE,
    )
    # Remove extra whitespace
    text = re.sub(r"\n{2,}", ". ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def text_to_speech(text: str, language: str = "en") -> Optional[bytes]:
    """
    Convert text to MP3 bytes using gTTS.
    Returns None if gTTS is unavailable or text is empty.
    """
    if not GTTS_AVAILABLE:
        return None
    if not text or not text.strip():
        return None

    clean = clean_text_for_speech(text)
    if len(clean) < 5:
        return None

    # gTTS has a limit; truncate if extremely long
    if len(clean) > 5000:
        clean = clean[:5000] + "... For more details, please scroll up."

    try:
        tts = gTTS(text=clean, lang=language, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None


def is_voice_available() -> bool:
    """Check if voice output is supported in this environment."""
    return GTTS_AVAILABLE
