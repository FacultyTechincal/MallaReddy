"""
Text to Voice (Text-to-Speech) App
Converts text into natural speech in many languages (incl. Indian
languages) using Google Text-to-Speech (gTTS). Needs internet,
but NO API key.
"""
from io import BytesIO

import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="Text to Voice", page_icon="🔊", layout="centered")

LANGUAGES = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
    "Bengali": "bn", "Marathi": "mr", "Kannada": "kn", "Malayalam": "ml",
    "Gujarati": "gu", "Urdu": "ur", "French": "fr", "Spanish": "es",
    "German": "de", "Japanese": "ja",
}

ACCENTS = {  # Only applies to English
    "Indian": "co.in",
    "American": "com",
    "British": "co.uk",
    "Australian": "com.au",
}

SAMPLES = {
    "English": "Hello! Welcome to my text to speech project. Have a great day.",
    "Hindi": "नमस्ते! मेरे टेक्स्ट टू स्पीच प्रोजेक्ट में आपका स्वागत है।",
    "Telugu": "నమస్కారం! నా టెక్స్ట్ టు స్పీచ్ ప్రాజెక్ట్‌కు స్వాగతం.",
}


def synthesize(text: str, lang: str, tld: str, slow: bool) -> bytes:
    buf = BytesIO()
    gTTS(text=text, lang=lang, tld=tld, slow=slow).write_to_fp(buf)
    return buf.getvalue()


# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
lang_name = st.sidebar.selectbox("Language", list(LANGUAGES.keys()))
accent = "Indian"
if lang_name == "English":
    accent = st.sidebar.selectbox("Accent", list(ACCENTS.keys()))
slow = st.sidebar.checkbox("Slow speech")
st.sidebar.caption("Tip: type the text in the same language you select.")

# ---------------- Main ----------------
st.title("🔊 Text to Voice")
st.write("Type or upload text and convert it to speech you can play and download.")

source = st.radio("Input type", ["Type text", "Upload .txt"], horizontal=True)
if source == "Type text":
    text = st.text_area(
        "Your text", value=SAMPLES.get(lang_name, ""), height=200, max_chars=5000
    )
else:
    file = st.file_uploader("Upload a .txt file", type=["txt"])
    text = file.read().decode("utf-8", errors="ignore") if file else ""
    if text:
        st.text_area("File content", text, height=200, disabled=True)

st.caption(f"{len(text)} characters")

if st.button("🔊 Convert to speech", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating audio..."):
            try:
                audio = synthesize(text, LANGUAGES[lang_name], ACCENTS[accent], slow)
            except Exception as e:
                st.error(f"Failed: {e}. Check your internet connection.")
                st.stop()
        st.success("Done!")
        st.audio(audio, format="audio/mp3")
        st.download_button("⬇️ Download MP3", audio, "speech.mp3", "audio/mpeg")
