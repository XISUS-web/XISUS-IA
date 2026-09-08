import streamlit as st
from openai import OpenAI
import base64

# ==============================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==============================================================================

st.set_page_config(
    page_title="XISUS IA",
    page_icon="👩‍🦲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ESTILO CSS
# ==============================================================================

st.markdown("""
    <style>

    .stApp {
        background-color: #ffffff;
        color: #1e293b;
    }

    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        border: none;
    }

    div.stButton > button:first-child:hover {
        background-color: #ff3333;
    }

    p, span, label {
        color: #334155 !important;
    }

    h1, h2, h3, h4 {
        color: #0f172a !important;
    }

    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. CONEXIÓN CON OPENAI
# ==============================================================================

try:

    API_KEY = st.secrets["OPENAI_API_KEY"]

    cliente = OpenAI(
        api_key=API_KEY
    )

except Exception:

    st.error(
        "🔑 Error: Configura 'OPENAI_API_KEY' "
        "en los Secrets de Streamlit."
    )

    st.stop()

# ==============================================================================
# 4. MEMORIA DEL CHAT
# ==============================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

# ==============================================================================
# 5. MEMORIA DE LA IMAGEN
# ==============================================================================

if "imagen_actual" not in st.session_state:
    st.session_state.imagen_actual = None

# ==============================================================================
# 6. PERSONALIDADES
# ==============================================================================

instrucciones = {

    "Normal":
        "Eres XISUS, tu calvito de confianza. "
        "Un asistente de IA útil, inteligente y claro.",

    "Amigable":
        "Eres XISUS, un asistente extremadamente amigable, "
        "entusiasta y cálido. Hablas de forma natural y cercana.",

    "Profesional":
        "Eres XISUS, un asistente serio, corporativo, "
        "formal, preciso y directo.",

    "Divertido":
        "Eres XISUS. Responde con mucho humor, bromas ligeras "
        "y buena onda, pero sin perder utilidad.",

    "Conciso":
        "Eres XISUS. Da respuestas extremadamente cortas, "
        "claras, al grano y sin rodeos."
}

# ==============================================================================
# 7. BARRA LATERAL
# ==============================================================================

with st.sidebar:

    st.markdown(
        "<h2 style='text-align: center;'>⚙️ Panel de Control</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------------------------
    # MODELO
    # --------------------------------------------------------------------------

    st.subheader("Parámetros del Modelo")

    modelo_visual = st.selectbox(
        "Selecciona el Cerebro:",
        [
            "gpt-5.6-luna",
            "gpt-5.6-terra",
            "gpt-5.6-sol"
        ],
        index=0
    )

    personalidad_visual = st.selectbox(
        "Estilo de Voz / Personalidad:",
        [
            "Normal",
            "Amigable",
            "Profesional",
            "Divertido",
            "Conciso"
        ]
    )

    # --------------------------------------------------------------------------
    # AJUSTES
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("Ajustes Avanzados")

    max_tokens = st.slider(
        "Longitud Máxima de Respuesta:",
        min_value=100,
        max_value=3000,
        value=1500,
        step=100
    )

    # --------------------------------------------------------------------------
    # IMÁGENES
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("📷 Imágenes")

modo_imagen = st.radio(
    "¿Quieres añadir una imagen?",
    [
        "Ninguna",
        "📁 Subir imagen",
        "📸 Usar cámara"
    ],
    index=0
)

imagen_subida = None
imagen_camara = None

if modo_imagen == "📁 Subir imagen":

    imagen_subida = st.file_uploader(
        "Selecciona una imagen",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],
        key="imagen_subida"
    )

elif modo_imagen == "📸 Usar cámara":

    imagen_camara = st.camera_input(
        "Haz una foto para XISUS",
        key="imagen_camara"
    )

imagen_nueva = (
    imagen_camara
    if imagen_camara is not None
    else imagen_subida
)

if imagen_nueva is not None:
    st.session_state.imagen_actual = imagen_nueva
