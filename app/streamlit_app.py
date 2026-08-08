#streamlit run ui/app.py
from __future__ import annotations

import os
import sys
from html import escape
from pathlib import Path

import streamlit as st
from streamlit_mic_recorder import mic_recorder
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


st.set_page_config(
    page_title="Cheerful Bot",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


MINT_CSS = """
<style>
    :root {
        --mint: #5eead4;
        --mint-soft: #d9fff6;
        --mint-pale: #effdf8;
        --ink: #17352f;
        --muted: #5e746f;
        --line: #c9efe5;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(94, 234, 212, 0.24), transparent 32rem),
            linear-gradient(180deg, #f7fffc 0%, #ffffff 46%, #f2fbf7 100%);
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d9fff6 0%, #f6fffc 100%);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: var(--ink) !important;
    }

    [data-baseweb="select"] > div {
        background: #f7fffc !important;
        border: 1px solid #86e7d3 !important;
        border-radius: 8px !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="select"] input {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
    }

    header[data-testid="stHeader"] {
        background: rgba(247, 255, 252, 0.92);
    }

    .hero {
        padding: 1.2rem 1.35rem;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.82);
        box-shadow: 0 12px 35px rgba(34, 120, 102, 0.08);
        margin-bottom: 1rem;
    }

    .hero-title {
        margin: 0;
        color: var(--ink);
        font-size: clamp(2rem, 3.5vw, 3.2rem);
        font-weight: 800;
        letter-spacing: 0;
    }

    .hero-subtitle {
        color: var(--muted);
        margin: 0.35rem 0 0;
        font-size: 1.02rem;
        max-width: 62rem;
        line-height: 1.55;
    }

    .status-row {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .status-pill {
        background: var(--mint-pale);
        border: 1px solid var(--line);
        border-radius: 999px;
        color: var(--ink);
        padding: 0.35rem 0.7rem;
        font-size: 0.88rem;
        font-weight: 650;
    }

    .section-label {
        color: var(--ink);
        font-weight: 750;
        margin-top: 1rem;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 8px;
        border: 1px solid rgba(201, 239, 229, 0.72);
        background: rgba(255, 255, 255, 0.78);
    }

    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] strong {
        color: var(--ink) !important;
    }

    div[data-testid="stChatInput"] textarea {
        border-color: var(--line);
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 8px;
        border: 1px solid #86e7d3;
        background: #e9fff9;
        color: var(--ink);
        font-weight: 700;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #20c7ac;
        color: #0d544a;
        background: #d9fff6;
    }

    [data-testid="stMetricValue"] {
        color: #0f766e;
    }

    [dir="rtl"] {
        direction: rtl;
        text-align: right;
    }
</style>
"""
st.markdown(MINT_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading Cheerful Bot...")
def load_engine():
    from core.cbr_engine import build_index, query as cbr_query
    from core.database import init_db

    csv_path = ROOT / "data" / "emotion_dataset_kaggle.csv"
    init_db(str(csv_path))
    build_index()
    return cbr_query


SUPPORTED_LANGUAGES: dict[str, str] = {
    "English": "en-US",
    "العربية": "ar-SA",
    "Français": "fr-FR",
}

VOICE_TO_LANG: dict[str, str] = {
    "en-US": "en",
    "ar-SA": "ar",
    "fr-FR": "fr",
}

UI = {
    "en": {
        "subtitle": "A cheerful mental-health companion that detects emotion and replies with simple support.",
        "welcome": (
            "Hi, I am **Cheerful Bot**. Tell me how you are feeling, and I will respond "
            "with a supportive suggestion. This is not medical advice, but I can help you reflect."
        ),
        "how_title": "How it works",
        "how_text": "Detect emotion, find a close case, respond kindly, then learn when you press thumbs up.",
        "clear": "Clear chat",
        "debug": "Show processing details",
        "type": "Type",
        "voice": "Voice",
        "input": "Tell me how you are feeling...",
        "thinking": "Thinking...",
        "detected": "Detected emotion",
        "translated": "Auto-translated from {lang}: {text}",
        "translation_failed": "Translation was not available, so the original text was used.",
        "record": "Record",
        "voice_ready": "Ready to listen in {lang}.",
        "up_toast": "Thanks, I saved that as a helpful answer.",
        "down_toast": "Thanks, I will try to do better next time.",
    },
    "ar": {
        "subtitle": "رفيق بسيط للصحة النفسية يكتشف المشاعر ويرد بدعم لطيف.",
        "welcome": (
            "أهلا، أنا **Cheerful Bot**. اكتب أو اتكلم عن إحساسك، وسأحاول أقدم لك رد داعم وبسيط. "
            "هذا ليس بديلا عن المساعدة الطبية، لكنه يساعدك على التعبير."
        ),
        "how_title": "طريقة العمل",
        "how_text": "يكتشف المشاعر، يبحث عن حالة قريبة، يرد بلطف، ويتعلم عند الضغط على إعجاب.",
        "clear": "مسح المحادثة",
        "debug": "عرض تفاصيل المعالجة",
        "type": "كتابة",
        "voice": "صوت",
        "input": "اكتب إحساسك هنا...",
        "thinking": "يفكر...",
        "detected": "المشاعر المكتشفة",
        "translated": "ترجمة تلقائية من {lang}: {text}",
        "translation_failed": "الترجمة غير متاحة، لذلك تم استخدام النص الأصلي.",
        "record": "تسجيل",
        "voice_ready": "جاهز للاستماع باللغة {lang}.",
        "up_toast": "شكرا، تم حفظ الرد كإجابة مفيدة.",
        "down_toast": "شكرا، سأحاول التحسن في المرة القادمة.",
    },
    "fr": {
        "subtitle": "Un compagnon simple qui détecte l'émotion et répond avec un soutien bienveillant.",
        "welcome": (
            "Bonjour, je suis **Cheerful Bot**. Dis-moi comment tu te sens, et je répondrai "
            "avec une suggestion de soutien. Ce n'est pas un avis médical, mais je peux t'aider à réfléchir."
        ),
        "how_title": "Fonctionnement",
        "how_text": "Détecte l'émotion, cherche un cas proche, répond avec bienveillance, puis apprend avec le pouce levé.",
        "clear": "Effacer le chat",
        "debug": "Afficher les détails",
        "type": "Écrire",
        "voice": "Voix",
        "input": "Dis-moi comment tu te sens...",
        "thinking": "Réflexion...",
        "detected": "Émotion détectée",
        "translated": "Traduit automatiquement depuis {lang} : {text}",
        "translation_failed": "La traduction n'était pas disponible, le texte original a été utilisé.",
        "record": "Enregistrer",
        "voice_ready": "Prêt à écouter en {lang}.",
        "up_toast": "Merci, j'ai enregistré cette réponse utile.",
        "down_toast": "Merci, j'essaierai de faire mieux la prochaine fois.",
    },
}

EMOTION_EMOJI = {
    "sadness": "😢",
    "anger": "😠",
    "hate": "😤",
    "empty": "😶",
    "anxiety": "🌧️",
    "neutral": "😐",
    "fun": "😄",
    "surprise": "😲",
    "enthusiasm": "🔥",
    "happiness": "😊",
    "love": "💕",
    "relief": "😌",
}

EMOTION_COLOR = {
    "sadness": "#3b82f6",
    "anger": "#dc2626",
    "hate": "#991b1b",
    "empty": "#64748b",
    "anxiety": "#6366f1",
    "neutral": "#64748b",
    "fun": "#f59e0b",
    "surprise": "#8b5cf6",
    "enthusiasm": "#ea580c",
    "happiness": "#10b981",
    "love": "#db2777",
    "relief": "#0d9488",
}


def reset_chat(ui_lang: str) -> None:
    st.session_state.messages = [
        {"role": "assistant", "content": UI[ui_lang]["welcome"], "meta": None}
    ]
    st.session_state.ui_lang = ui_lang


def render_meta(meta: dict, labels: dict[str, str], debug_mode: bool) -> None:
    emotion = meta.get("emotion", "neutral")
    confidence = float(meta.get("confidence", 0))
    color = EMOTION_COLOR.get(emotion, "#64748b")
    emoji = EMOTION_EMOJI.get(emotion, "💬")
    st.markdown(
        f"<small style='color:{color};font-weight:700'>{emoji} "
        f"{escape(labels['detected'])}: {escape(emotion)} ({confidence * 100:.0f}%)</small>",
        unsafe_allow_html=True,
    )

    detected_lang = meta.get("detected_lang", "en")
    translated_text = meta.get("translated_text", "")
    if detected_lang != "en" and translated_text:
        if meta.get("translation_ok", True):
            st.caption(labels["translated"].format(lang=detected_lang.upper(), text=translated_text))
        else:
            st.caption(labels["translation_failed"])

    if debug_mode and meta.get("debug_steps"):
        with st.expander("Processing details", expanded=False):
            st.json(meta["debug_steps"])

def get_voice_text(lang_name: str, voice_code: str, labels: dict[str, str]) -> str | None:
    col_record, col_hint = st.columns([1, 4])
    with col_record:
        audio = mic_recorder(
            start_prompt=f"Record 🎙️",
            stop_prompt="Stop 🛑",
            key="mic_rec"
        )
    with col_hint:
        st.caption(labels["voice_ready"].format(lang=lang_name))

    if audio:
        st.audio(audio["bytes"])
        st.info("Audio received. If you have a speech-to-text model, connect audio['bytes'] to it.")
        return None

    return None

with st.sidebar:
    st.title("🌿 Cheerful Bot")
    st.caption("Emotion CBR assistant")

    st.markdown('<p class="section-label">Language</p>', unsafe_allow_html=True)
    lang_name = st.selectbox(
        "Language",
        list(SUPPORTED_LANGUAGES.keys()),
        index=0,
        label_visibility="collapsed",
    )
    voice_code = SUPPORTED_LANGUAGES[lang_name]
    ui_lang = VOICE_TO_LANG[voice_code]
    labels = UI[ui_lang]

    st.markdown('<p class="section-label">Input</p>', unsafe_allow_html=True)
    input_mode = st.radio(
        "Input mode",
        [labels["type"], labels["voice"]],
        horizontal=True,
        label_visibility="collapsed",
    )

    debug_mode = st.toggle(labels["debug"], value=False)

    st.markdown("---")
    st.subheader(labels["how_title"])
    st.write(labels["how_text"])

    if st.button(labels["clear"], use_container_width=True):
        reset_chat(ui_lang)
        st.rerun()


direction = "rtl" if ui_lang == "ar" else "ltr"
st.markdown(
    f"""
    <div class="hero" dir="{direction}">
        <h1 class="hero-title">Cheerful Bot</h1>
        <p class="hero-subtitle">{escape(labels["subtitle"])}</p>
        <div class="status-row">
            <span class="status-pill">Mint green UI</span>
            <span class="status-pill">Emotion detection</span>
            <span class="status-pill">Case-based response</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

cbr_query = load_engine()

if "messages" not in st.session_state or st.session_state.get("ui_lang") != ui_lang:
    reset_chat(ui_lang)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        meta = message.get("meta")
        if meta:
            render_meta(meta, labels, debug_mode)


if input_mode == labels["voice"]:
    user_text = get_voice_text(lang_name, voice_code, labels)
else:
    user_text = st.chat_input(labels["input"])


if user_text and user_text.strip():
    user_text = user_text.strip()
    st.session_state.messages.append({"role": "user", "content": user_text, "meta": None})

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner(labels["thinking"]):
            result = cbr_query(user_input=user_text, ui_lang=ui_lang, debug=False)

        response = result["response"]
        emotion = result["category"]
        confidence = float(result["confidence"])
        meta = {
            "emotion": emotion,
            "confidence": confidence,
            "detected_lang": result.get("detected_lang", "en"),
            "translated_text": result.get("translated_text", user_text),
            "translation_ok": result.get("translation_ok", True),
            "debug_steps": {
                "original": user_text,
                "detected_lang": result.get("detected_lang", "en"),
                "translated_text": result.get("translated_text", user_text),
                "cleaned_text": result.get("cleaned_text", ""),
                "emotion": emotion,
                "confidence": confidence,
                "detector": result.get("source", "model"),
                "similarity_score": result.get("score", 0),
            },
        }

        st.markdown(response)
        render_meta(meta, labels, debug_mode)

        col_up, col_down, _ = st.columns([1, 1, 8])
        feedback_key = len(st.session_state.messages)
        with col_up:
            if st.button("👍", key=f"up_{feedback_key}"):
                from core.cbr_engine import retain

                retain(user_text, response, emotion)
                st.toast(labels["up_toast"])
        with col_down:
            if st.button("👎", key=f"down_{feedback_key}"):
                st.toast(labels["down_toast"])

    st.session_state.messages.append(
        {"role": "assistant", "content": response, "meta": meta}
    )
