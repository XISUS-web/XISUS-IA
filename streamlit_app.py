import streamlit as st
from openai import OpenAI

# ==============================================================================
# 1. CONFIGURACIÓN ESTÉTICA DE LA PÁGINA
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
    cliente = OpenAI(api_key=API_KEY)

except Exception as e:
    st.error(
        "🔑 Error: Configura 'OPENAI_API_KEY' en los Secrets de Streamlit."
    )
    st.stop()

# ==============================================================================
# 4. MEMORIA DEL CHAT
# ==============================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

# ==============================================================================
# 5. BARRA LATERAL
# ==============================================================================

with st.sidebar:

    st.markdown(
        "<h2 style='text-align: center;'>⚙️ Panel de Control</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

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

    st.markdown("---")

    st.subheader("Ajustes Avanzados")

    temperatura = st.slider(
        "Creatividad (Temperatura):",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )

    max_tokens = st.slider(
        "Longitud Máxima de Respuesta:",
        min_value=100,
        max_value=3000,
        value=1500,
        step=100
    )

    st.markdown("---")

    if st.button(
        "🗑️ Limpiar Historial de Chat",
        use_container_width=True
    ):
        st.session_state.historial = []
        st.rerun()

    st.markdown("---")

    st.subheader("💬 Estado de XISUS")
    st.success("🟢 API OpenAI Conectada")

# ==============================================================================
# 6. PANTALLA CENTRAL
# ==============================================================================

URL_DE_TU_IMAGEN = (
    "https://i.postimg.cc/Gmx2FfpG/IMG-2-20260818-WA0020.jpg"
)

st.image(
    URL_DE_TU_IMAGEN,
    width=200
)

st.markdown(
    "<h1 style='color: #ff4b4b; margin-top: 10px; margin-bottom: 0;'>"
    "👩‍🦲 XISUS IA"
    "</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='font-size: 18px; color: #64748b;'>"
    "Tu asistente de inteligencia artificial de confianza."
    "</p>",
    unsafe_allow_html=True
)

st.write(
    "XISUS IA es un asistente de inteligencia artificial capaz de responder "
    "preguntas, ayudarte con tareas, generar ideas y mantener conversaciones. "
    "Habla con XISUS y obtén respuestas rápidas y útiles."
)

st.markdown("---")

# ==============================================================================
# 7. PERSONALIDADES
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
# 8. MOSTRAR HISTORIAL
# ==============================================================================

for mensaje in st.session_state.historial:

    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# ==============================================================================
# 9. INPUT DEL CHAT
# ==============================================================================

pregunta = st.chat_input(
    "Escribe tu consulta aquí para hablar con tu calvito..."
)

# ==============================================================================
# 10. PROCESAMIENTO DE LA PREGUNTA
# ==============================================================================

if pregunta:

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Guardar mensaje del usuario
    st.session_state.historial.append({
        "role": "user",
        "content": pregunta
    })

    try:

        # Solo enviamos las últimas 16 intervenciones
        historial_limitado = st.session_state.historial[-16:]

        # ======================================================================
        # RESPUESTA DE XISUS CON STREAMING
        # ======================================================================

        with st.chat_message("assistant"):

           stream = cliente.responses.create(
               model=modelo_visual,
               instructions=instrucciones[personalidad_visual],
               input=historial_limitado,
               max_output_tokens=max_tokens,
               stream=True
           )

            respuesta_completa = ""

            placeholder = st.empty()

            for evento in stream:

                if evento.type == "response.output_text.delta":

                    respuesta_completa += evento.delta

                    placeholder.markdown(respuesta_completa)

        # ======================================================================
        # GUARDAR RESPUESTA
        # ======================================================================

        st.session_state.historial.append({
            "role": "assistant",
            "content": respuesta_completa
        })

    except Exception as e:

        st.error(
            "😕 Ocurrió un inconveniente técnico al contactar "
            "con la inteligencia artificial."
        )

        st.caption(f"Error detectado: {e}")
