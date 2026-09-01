import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURACIÓN ESTÉTICA DE LA PÁGINA (Modo ancho para mejor visualización)
st.set_page_config(
    page_title="XISUS IA", 
    page_icon="👩‍🦲", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para mejorar el diseño visual y los contenedores
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #e2e8f0; }
    .sidebar .sidebar-content { background-color: #1a1f2c; }
    div.stButton > button:first-child {
        background-color: #ff4b4b; color: white; border-radius: 8px; border: none;
    }
    div.stButton > button:first-child:hover { background-color: #ff3333; }
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
# 4. BARRA LATERAL IZQUIERDA: CONFIGURACIONES AVANZADAS (MÁS OPCIONES Y ESTÉTIICA)
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
    
    # NUEVA OPCIÓN: Control de Creatividad (Temperatura)
    temperatura = st.slider(
        "Creatividad (Temperatura):", 
        min_value=0.0, max_value=2.0, value=0.7, step=0.1,
        help="Valores altos dan respuestas más creativas; valores bajos son más precisos."
    )
    
    # NUEVA OPCIÓN: Límite de longitud de la respuesta
    max_tokens = st.slider(
        "Longitud Máxima de Respuesta (Tokens):", 
        min_value=100, max_value=2000, value=800, step=100,
        help="Controla el tamaño máximo del texto que generará la IA."
    )
    
    st.markdown("---")
    # Botón estético y funcional para reiniciar la conversación
    if st.button("🗑️ Limpiar Historial de Chat", use_container_width=True):
        st.session_state.historial_google = []
        st.rerun()
        
    st.markdown("---")
    st.subheader("💬 Estado de XISUS")
    st.success("🟢 API Google Conectada")
    st.info(f"🧠 Activo: {modelo_visual}")
    st.info(f"🎨 Estilo: {personalidad_visual}")

# ==============================================================================
# 5. PANTALLA CENTRAL: INTERFAZ DE USUARIO LIMPIA Y MODERNA
# ==============================================================================
st.markdown("<h1 style='text-align: center; color: #ff4b4b; margin-bottom: 0;'>👩‍🦲 XISUS IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #8892b0;'>Tu calvito de confianza en una interfaz premium</p>", unsafe_allow_html=True)
st.markdown("---")

# Mapeo dinámico de personalidades según el diccionario
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

# Input del chat colocado de forma elegante abajo
pregunta = st.chat_input("Escribe tu consulta aquí para hablar con tu calvito...")

# 6. LÓGICA DE EJECUCIÓN CON CONFIGURACIÓN AVANZADA EXPANDIDA
if pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    
    parte_nativa = types.Part.from_text(text=pregunta)
    mensaje_nativo = types.Content(role="user", parts=[parte_nativa])
    st.session_state.historial_google.append(mensaje_nativo)

    try:
        # Añadimos los nuevos parámetros avanzados a la configuración de contenido
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
