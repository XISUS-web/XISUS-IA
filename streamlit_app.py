import streamlit as st
st.set_page_config(
    page_title="Xisus IA",
    page_icon="🤖",
    layout="centered"
)
from google import genai
from google.genai import types

# 1. CONFIGURACIÓN ESTÉTICA DE LA PÁGINA (Tema Claro Premium)
st.set_page_config(
    page_title="XISUS IA", 
    page_icon="👩‍🦲", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para cambiar el fondo a BLANCO y adaptar textos
st.markdown("""
    <style>
    /* Fondo principal blanco y textos oscuros */
    .stApp { 
        background-color: #ffffff; 
        color: #1e293b; 
    }
    /* Estilo para la barra lateral (Gris claro muy limpio) */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    /* Botón de borrar historial en color rojo estético */
    div.stButton > button:first-child {
        background-color: #ff4b4b; 
        color: white; 
        border-radius: 8px; 
        border: none;
    }
    div.stButton > button:first-child:hover { 
        background-color: #ff3333; 
    }
    /* Forzar que los textos secundarios se lean bien en fondo blanco */
    p, span, label {
        color: #334155 !important;
    }
    h1, h2, h3, h4 {
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. INICIALIZACIÓN SEGURA DE LA API
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    cliente = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🔑 Error: Configura 'GEMINI_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. MEMORIA INTERNA DEL CHAT
if "historial_google" not in st.session_state:
    st.session_state.historial_google = []

# ==============================================================================
# 4. BARRA LATERAL IZQUIERDA: CONFIGURACIONES AVANZADAS
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Panel de Control</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🤖 Parámetros del Modelo")
    modelo_visual = st.selectbox(
        "Selecciona el Cerebro:",
        ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.5-flash"]
    )
    
    personalidad_visual = st.selectbox(
        "Estilo de Voz / Personalidad:",
        ["Normal", "Amigable", "Profesional", "Divertido", "Conciso"]
    )
    
    st.markdown("---")
    st.subheader("🎛️ Ajustes Avanzados")
    
    temperatura = st.slider(
        "Creatividad (Temperatura):", 
        min_value=0.0, max_value=2.0, value=0.7, step=0.1
    )
    
    max_tokens = st.slider(
        "Longitud Máxima de Respuesta (Tokens):", 
        min_value=100, max_value=2000, value=800, step=100
    )
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Historial de Chat", use_container_width=True):
        st.session_state.historial_google = []
        st.rerun()
        
    st.markdown("---")
    st.subheader("💬 Estado de XISUS")
    st.success("🟢 API Google Conectada")

# ==============================================================================
# 5. PANTALLA CENTRAL: IMAGEN Y CHAT
# ==============================================================================

# --- AQUÍ VA TU IMAGEN ---
# Puedes usar un enlace de internet directo (URL) o la ruta de un archivo local en tu GitHub
URL_DE_TU_IMAGEN = "https://flaticon.com" 

# Desplegamos la imagen centrada y con un tamaño estético de 200 píxeles
st.image(URL_DE_TU_IMAGEN, width=200, use_container_width=False)

st.markdown("<h1 style='color: #ff4b4b; margin-top: 10px; margin-bottom: 0;'>👩‍🦲 XISUS IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px; color: #64748b;'>Tu calvito de confianza en modo claro premium</p>", unsafe_allow_html=True)
st.markdown("---")

# Mapeo dinámico de personalidades
instrucciones = {
    "Normal": "Eres XISUS, tu calvito de confianza. Un asistente de IA útil.",
    "Amigable": "Eres XISUS, un asistente extremadamente amigable, entusiasta y cálido.",
    "Profesional": "Eres XISUS, un asistente serio, corporativo, formal y directo.",
    "Divertido": "Eres XISUS. Responde con mucho humor, bromas ligeras y buena onda.",
    "Conciso": "Eres XISUS. Da respuestas extremadamente cortas, al grano y sin rodeos."
}

# Dibujar el historial de mensajes de forma elegante en la zona central
for mensaje in st.session_state.historial_google:
    rol_visual = "user" if mensaje.role == "user" else "assistant"
    with st.chat_message(rol_visual):
        for parte in mensaje.parts:
            if parte.text:
                st.write(parte.text)

# Input del chat colocado abajo
pregunta = st.chat_input("Escribe tu consulta aquí para hablar con tu calvito...")

# 6. LÓGICA DE EJECUCIÓN
if pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    
    parte_nativa = types.Part.from_text(text=pregunta)
    mensaje_nativo = types.Content(role="user", parts=[parte_nativa])
    st.session_state.historial_google.append(mensaje_nativo)

    try:
        configuracion = types.GenerateContentConfig(
            system_instruction=instrucciones[personalidad_visual],
            temperature=temperatura,
            max_output_tokens=max_tokens
        )

        with st.spinner("XISUS está procesando tu respuesta..."):
            resultado = cliente.models.generate_content(
                model=modelo_visual,
                contents=st.session_state.historial_google,
                config=configuracion
            )

        with st.chat_message("assistant"):
            st.write(resultado.text)
        
        parte_respuesta = types.Part.from_text(text=resultado.text)
        respuesta_nativa = types.Content(role="model", parts=[parte_respuesta])
        st.session_state.historial_google.append(respuesta_nativa)
        
        st.rerun()

    except Exception as e:
        st.error("😕 Ocurrió un inconveniente técnico al contactar a la inteligencia artificial.")
        st.caption(f"Error detectado: {e}")
