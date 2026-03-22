import streamlit as st
import requests
import io
import docx
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(
    page_title="Sunflower: Uganda Connect", 
    page_icon="🌻", 
    layout="centered"
)

# 2. Injecting Tailwind, FontAwesome, Google Fonts, and Custom CSS bindings
st.markdown("""
<!-- Load Tailwind CSS via CDN -->
<script src="https://cdn.tailwindcss.com"></script>
<!-- Load FontAwesome via CDN -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<!-- Load Outfit Font -->
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">

<style>
    /* Ugandan Flag Decorative Top Border */
    .stApp > header {
        border-top: 4px solid transparent;
        border-image: repeating-linear-gradient(
            45deg,
            #000000,
            #000000 20px,
            #FCE205 20px,
            #FCE205 40px,
            #D90000 40px,
            #D90000 60px
        ) 1;
    }

    /* Background and global font */
    .stApp {
        background-color: #0f172a; /* bg-slate-900 */
        color: #f8fafc; /* text-slate-50 */
        font-family: 'Outfit', sans-serif;
    }

    /* Pill-styled Tabs override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b; /* bg-slate-800 */
        color: #94a3b8; /* text-slate-400 */
        border: 1px solid #334155; /* border-slate-700 */
        border-radius: 9999px; /* rounded-full */
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ea580c !important; /* bg-orange-600 */
        color: white !important;
        border-color: #f97316 !important; /* border-orange-500 */
        box-shadow: 0 4px 14px 0 rgba(249, 115, 22, 0.5) !important; /* shadow-orange-500/50 */
    }

    /* Dropzone (File Uploader) override */
    div[data-testid="stFileUploader"] section {
        background-color: #0f172a; /* bg-slate-900 */
        border: 2px dashed #334155; /* border-slate-700 */
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    div[data-testid="stFileUploader"] section:hover {
        border-color: #ea580c; /* hover:border-orange-600 */
        background-color: #1e293b;
    }

    /* Buttons Override (Primary Action) */
    .stButton > button {
        background-color: #ea580c; /* bg-orange-600 */
        color: white;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #c2410c; /* hover:bg-orange-700 */
        box-shadow: 0 4px 14px 0 rgba(249, 115, 22, 0.4);
    }

    /* Input Fields Override */
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b !important; /* bg-slate-800 */
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #f97316 !important; /* border-orange-500 */
        box-shadow: 0 0 0 1px #f97316 !important;
    }

    /* Result Panes styling */
    .translation-box {
        background-color: #1e293b;
        border-left: 4px solid #ea580c; /* border-orange-600 */
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
        color: #f59e0b; /* text-amber-500 */
        font-weight: 600;
        font-size: 1.1rem;
    }
    .original-box {
        background-color: #0f172a;
        border-left: 4px solid #64748b; /* border-slate-500 */
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to generate SVG language badges
def get_lang_badge(initial, color="#f59e0b"): # Default amber
    svg = f'''<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="10" fill="none" stroke="{color}" stroke-width="2"/>
      <text x="12" y="16.5" font-family="Outfit, sans-serif" font-weight="bold" font-size="14" fill="{color}" text-anchor="middle">{initial}</text>
    </svg>'''
    return svg

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("<h2 style='font-family: Outfit; font-weight: 800; color: #f8fafc;'><i class='fa-solid fa-gear' style='color:#94a3b8; margin-right:8px;'></i> Hub Settings</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Authenticate with Sunbird AI.</p>", unsafe_allow_html=True)
    api_key = st.text_input("Enter Sunbird API Key", type="password")
    
    st.markdown("<hr style='border-color: #334155'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #e2e8f0; font-weight: 600;'><i class='fa-solid fa-earth-africa' style='color:#f59e0b; margin-right:8px;'></i> Supported Languages:</p>", unsafe_allow_html=True)
    
    # Custom HTML list with SVG Badges instead of Emojis
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; font-family: Outfit;">
        <div style="display: flex; align-items: center; gap: 12px;">{get_lang_badge('L', color="#eab308")} <span style="color:#cbd5e1; font-weight:600">Luganda</span></div>
        <div style="display: flex; align-items: center; gap: 12px;">{get_lang_badge('L', color="#3b82f6")} <span style="color:#cbd5e1; font-weight:600">Luo</span></div>
        <div style="display: flex; align-items: center; gap: 12px;">{get_lang_badge('A', color="#10b981")} <span style="color:#cbd5e1; font-weight:600">Ateso</span></div>
        <div style="display: flex; align-items: center; gap: 12px;">{get_lang_badge('R', color="#8b5cf6")} <span style="color:#cbd5e1; font-weight:600">Runyankole</span></div>
        <div style="display: flex; align-items: center; gap: 12px;">{get_lang_badge('L', color="#14b8a6")} <span style="color:#cbd5e1; font-weight:600">Lugbara</span></div>
        <div style="display: flex; align-items: center; gap: 12px;">{get_lang_badge('L', color="#06b6d4")} <span style="color:#cbd5e1; font-weight:600">Lusoga</span></div>
    </div>
    """, unsafe_allow_html=True)

# 4. Main UI Header (Tailwind injected classes)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2.5rem; background: linear-gradient(to right, #fb923c, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Sunflower: Uganda Connect
    </h1>
    <p style="color: #94a3b8; font-size: 1.1rem; font-family: 'Outfit', sans-serif;">The All-in-One Local Uganda AI Hub</p>
</div>
""", unsafe_allow_html=True)

# 5. Multi-Modal Input Module
# Removing emojis and using clean text for native Streamlit Tabs
tab1, tab2, tab3 = st.tabs(["TEXT", "FILE UPLOAD", "AUDIO / VOICE"])

text_input = ""
extracted_text = ""
audio_bytes = None
uploaded_audio = None

with tab1:
    st.markdown("<div style='margin-bottom: 8px; font-family: Outfit; font-weight: 600; color:#f59e0b'><i class='fa-solid fa-align-left' style='margin-right: 8px;'></i> Enter Text</div>", unsafe_allow_html=True)
    text_input = st.text_area(
        "Enter English text for translation:", 
        placeholder="e.g., Welcome to our beautiful village, we are so happy to see you.", 
        height=130,
        label_visibility="collapsed"
    )

with tab2:
    st.markdown("""
    <div style='text-align:center; padding: 30px; font-family: Outfit;'>
        <i class='fa-solid fa-file-arrow-up' style='font-size: 2.5rem; color: #94a3b8; margin-bottom: 12px;'></i>
        <h3 style='color: #f8fafc; font-weight: 600; font-size: 1.5rem; margin-bottom: 8px;'>Upload .doc, .pdf, or .txt</h3>
        <p style='color: #64748b;'>The system will extract the document structure for translation.</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.pdf'):
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    extracted_text += page.extract_text() + "\n"
            elif uploaded_file.name.endswith('.docx'):
                doc = docx.Document(uploaded_file)
                for para in doc.paragraphs:
                    extracted_text += para.text + "\n"
            elif uploaded_file.name.endswith('.txt'):
                extracted_text = uploaded_file.getvalue().decode("utf-8")
            
            if extracted_text.strip():
                st.success("✅ Document loaded and extracted successfully!")
                with st.expander("Preview extracted text"):
                    preview = extracted_text[:300] + "..." if len(extracted_text) > 300 else extracted_text
                    st.text(preview)
        except Exception as e:
            st.error(f"Error reading file: {e}")

with tab3:
    st.markdown("""
    <div style='text-align:center; padding: 30px; font-family: Outfit;'>
        <i class='fa-solid fa-microphone-lines' style='font-size: 2.5rem; color: #ea580c; margin-bottom: 12px;'></i>
        <h3 style='color: #f59e0b; font-weight: 600; font-size: 1.5rem; margin-bottom: 8px;'>Listening...</h3>
        <p style='color: #94a3b8;'>(Luo, Ateso, Swahili, and more)</p>
    </div>
    """, unsafe_allow_html=True)
    colA, colB = st.columns(2)
    
    # Initialize a session state key for the audio input if it doesn't exist
    if "audio_key" not in st.session_state:
        st.session_state.audio_key = 0
        
    with colA:
        audio_bytes = st.audio_input("Record your voice", label_visibility="collapsed", key=f"record_mic_{st.session_state.audio_key}")
        if st.button("🔄 Discard & Record Another", use_container_width=True):
            st.session_state.audio_key += 1
            st.rerun()
            
    with colB:
        uploaded_audio = st.file_uploader("Upload Audio File (.mp3, .wav)", type=["mp3", "wav"], label_visibility="collapsed")

# 6. Global Target Selector & Action Button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div style='margin-bottom: 8px; font-family: Outfit; font-weight: 600; color:#94a3b8'><i class='fa-solid fa-language' style='margin-right: 8px;'></i> Target Language</div>", unsafe_allow_html=True)
    target_lang = st.selectbox(
        "Target Language",
        ["Luganda", "Runyankole", "Ateso", "Luo", "Lugbara", "Lusoga"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
    translate_pressed = st.button("Translate Now")

st.markdown("---")

LANG_CODES = {
    "Luganda": "lug",
    "Runyankole": "nyn",
    "Ateso": "teo",
    "Luo": "ach",
    "Lugbara": "lgg",
    "Lusoga": "xog"
}

# 7. Translation Logic & Output Module
if translate_pressed:
    # Check if an audio file was provided (Audio takes highest precedence)
    audio_input_data = audio_bytes if audio_bytes else uploaded_audio
    text_to_translate = extracted_text.strip() if extracted_text.strip() else text_input.strip()

    if not api_key:
        st.error("Please enter your API Key in the sidebar Settings!")
        st.stop()
        
    if audio_input_data is not None:
        with st.spinner("Transcribing audio..."):
            stt_url = "https://api.sunbird.ai/tasks/stt"
            stt_headers = {"Authorization": f"Bearer {api_key}"}
            # Pass the file directly using its name and bytes
            files = {"audio": (audio_input_data.name, audio_input_data.getvalue(), "audio/wav")}
            try:
                stt_response = requests.post(stt_url, headers=stt_headers, files=files)
                if stt_response.status_code == 200:
                    stt_json = stt_response.json()
                    text_to_translate = stt_json.get("audio_transcription", "")
                    
                    st.success("Audio transcribed successfully!")
                else:
                    st.error(f"STT Error ({stt_response.status_code}): {stt_response.text}")
                    st.stop()
            except Exception as e:
                st.error(f"Error connecting to STT: {e}")
                st.stop()

    if not text_to_translate:
        st.warning("Please enter text, upload a document, or record audio to translate.")
    else:
        with st.spinner(f"Translating to {target_lang}..."):
            url = "https://api.sunbird.ai/tasks/sunflower_inference"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "messages": [
                    {"role": "system", "content": f"You are a professional translator. Translate the following English text into {target_lang}."},
                    {"role": "user", "content": text_to_translate}
                ],
                "model_type": "qwen"
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    st.error(f"API Error ({response.status_code}): {response.text}")
                else:
                    result = response.json()
                    
                    if 'content' in result:
                        translation = result['content']
                        
                        st.markdown("<h3 style='font-family: Outfit; color: #f8fafc; font-weight: 800;'><i class='fa-solid fa-sparkles' style='color:#ea580c; margin-right:8px;'></i> Results</h3>", unsafe_allow_html=True)
                        res_col1, res_col2 = st.columns(2)
                        
                        with res_col1:
                            st.caption("Original text (English):")
                            preview_text = text_to_translate[:500] + "..." if len(text_to_translate) > 500 else text_to_translate
                            st.markdown(f"<div class='original-box'>{preview_text}</div>", unsafe_allow_html=True)
                            
                        with res_col2:
                            st.caption(f"Translated to ({target_lang}):")
                            st.markdown(f"<div class='translation-box'>{translation}</div>", unsafe_allow_html=True)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            with st.spinner("Generating audio..."):
                                tts_url = "https://api.sunbird.ai/tasks/tts"
                                tts_payload = {
                                    "text": translation,
                                    "language": LANG_CODES.get(target_lang, "lug")
                                }
                                try:
                                    tts_resp = requests.post(tts_url, headers=headers, json=tts_payload)
                                    if tts_resp.status_code == 200:
                                        content_type = tts_resp.headers.get("Content-Type", "")
                                        if "application/json" in content_type:
                                            tts_json = tts_resp.json()
                                            
                                            # The audio_url is nested inside the 'output' dictionary
                                            output_data = tts_json.get("output", {})
                                            audio_data = output_data.get("audio_url") or tts_json.get("audio_url")
                                            
                                            if audio_data:
                                                if isinstance(audio_data, str) and audio_data.startswith("http"):
                                                    st.audio(audio_data)
                                                else:
                                                    import base64
                                                    st.audio(base64.b64decode(audio_data), format="audio/wav")
                                            else:
                                                st.warning("TTS API didn't return an expected audio format.")
                                        else:
                                            # Raw binary audio
                                            st.audio(tts_resp.content, format="audio/wav")
                                    else:
                                        st.warning(f"Audio Playback Error: ({tts_resp.status_code}) {tts_resp.text}")
                                except Exception as e:
                                    st.error(f"TTS Exception: {e}")
                            
                    else:
                        st.error("The API returned an unexpected response format:")
                        st.json(result)
                
            except Exception as e:
                st.error(f"Error: {e}")