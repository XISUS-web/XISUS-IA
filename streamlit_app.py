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

except Exception as e:

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
# 5. MEMORIA DE LA IMAGEN ACTUAL
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
            "No, callate:(",
            "📁 Subir imagen",
            "📸 Usar cámara"
        ],
        index=0
    )

    # --------------------------------------------------------------------------
    # SUBIR IMAGEN
    # --------------------------------------------------------------------------

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

    # --------------------------------------------------------------------------
    # CÁMARA
    # --------------------------------------------------------------------------

    elif modo_imagen == "📸 Usar cámara":

        imagen_camara = st.camera_input(
            "Haz una foto para XISUS",
            key="imagen_camara"
        )

    # --------------------------------------------------------------------------
    # SELECCIONAR IMAGEN
    # --------------------------------------------------------------------------

    imagen_nueva = (
        imagen_camara
        if imagen_camara is not None
        else imagen_subida
    )

    if imagen_nueva is not None:

        st.session_state.imagen_actual = imagen_nueva

    # --------------------------------------------------------------------------
    # QUITAR IMAGEN
    # --------------------------------------------------------------------------

    if st.session_state.imagen_actual is not None:

        if st.button(
            "🗑️ Quitar imagen",
            use_container_width=True
        ):

            st.session_state.imagen_actual = None

            st.rerun()

    # --------------------------------------------------------------------------
    # LIMPIAR HISTORIAL
    # --------------------------------------------------------------------------

    st.markdown("---")

    if st.button(
        "🗑️ Limpiar Historial de Chat",
        use_container_width=True
    ):

        st.session_state.historial = []

        st.rerun()

    # --------------------------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("💬 Estado de XISUS")

    st.success(
        "🟢 API OpenAI Conectada"
    )

# ==============================================================================
# 8. PANTALLA CENTRAL
# ==============================================================================

URL_DE_TU_IMAGEN = (
    "https://i.postimg.cc/Gmx2FfpG/IMG-2-20260818-WA0020.jpg"
)

st.image(
    URL_DE_TU_IMAGEN,
    width=200
)

st.markdown(
    "<h1 style='color: #ff4b4b; "
    "margin-top: 10px; margin-bottom: 0;'>"
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
    "XISUS IA es un asistente de inteligencia artificial "
    "capaz de responder preguntas, ayudarte con tareas, "
    "generar ideas y mantener conversaciones. "
    "Habla con XISUS y obtén respuestas rápidas y útiles."
)

st.markdown("---")

# ==============================================================================
# 9. MOSTRAR IMAGEN SELECCIONADA
# ==============================================================================

imagen = st.session_state.imagen_actual

if imagen is not None:

    st.markdown("### 📷 Imagen seleccionada")

    st.image(
        imagen,
        caption="Esta es la imagen que verá XISUS",
        width=400
    )

# ==============================================================================
# 10. MOSTRAR HISTORIAL
# ==============================================================================

for mensaje in st.session_state.historial:

    with st.chat_message(
        mensaje["role"]
    ):

        st.markdown(
            mensaje["content"]
        )

# ==============================================================================
# 11. INPUT DEL CHAT
# ==============================================================================

pregunta = st.chat_input(
    "Escribe tu consulta aquí para hablar con tu calvito..."
)

# ==============================================================================
# 12. PROCESAMIENTO DE LA PREGUNTA
# ==============================================================================

if pregunta:

    # --------------------------------------------------------------------------
    # MOSTRAR MENSAJE DEL USUARIO
    # --------------------------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            pregunta
        )

        if imagen is not None:

            st.image(
                imagen,
                width=400
            )

    try:

        # ======================================================================
        # PREPARAR CONTENIDO
        # ======================================================================

        if imagen is not None:

            # --------------------------------------------------------------
            # CONVERTIR IMAGEN A BASE64
            # --------------------------------------------------------------

            imagen_bytes = imagen.getvalue()

            imagen_base64 = base64.b64encode(
                imagen_bytes
            ).decode("utf-8")

            # --------------------------------------------------------------
            # OBTENER TIPO MIME
            # --------------------------------------------------------------

            tipo_imagen = imagen.type

            # --------------------------------------------------------------
            # CREAR DATA URL
            # --------------------------------------------------------------

            imagen_data_url = (
                f"data:{tipo_imagen};base64,{imagen_base64}"
            )

            # --------------------------------------------------------------
            # TEXTO + IMAGEN
            # --------------------------------------------------------------

            contenido_usuario = [

                {
                    "type": "input_text",
                    "text": pregunta
                },

                {
                    "type": "input_image",
                    "image_url": imagen_data_url,
                    "detail": "auto"
                }

            ]

        else:

            # --------------------------------------------------------------
            # SOLO TEXTO
            # --------------------------------------------------------------

            contenido_usuario = pregunta

        # ======================================================================
        # CREAR HISTORIAL PARA OPENAI
        # ======================================================================

        historial_limitado = (
            st.session_state.historial[-16:]
        )

        historial_para_openai = (
            historial_limitado
            +
            [
                {
                    "role": "user",
                    "content": contenido_usuario
                }
            ]
        )

        # ======================================================================
        # GENERAR RESPUESTA
        # ======================================================================

        with st.chat_message("assistant"):

            stream = cliente.responses.create(

                model=modelo_visual,

                instructions=(
                    instrucciones[
                        personalidad_visual
                    ]
                ),

                input=historial_para_openai,

                max_output_tokens=max_tokens,

                stream=True
            )

            # --------------------------------------------------------------
            # ACUMULAR RESPUESTA
            # --------------------------------------------------------------

            respuesta_completa = ""

            placeholder = st.empty()

            # --------------------------------------------------------------
            # STREAMING
            # --------------------------------------------------------------

            for evento in stream:

                if (
                    evento.type
                    ==
                    "response.output_text.delta"
                ):

                    respuesta_completa += (
                        evento.delta
                    )

                    placeholder.markdown(
                        respuesta_completa
                    )

        # ======================================================================
        # GUARDAR PREGUNTA
        # ======================================================================

        st.session_state.historial.append(
            {
                "role": "user",
                "content": pregunta
            }
        )

        # ======================================================================
        # GUARDAR RESPUESTA
        # ======================================================================

        st.session_state.historial.append(
            {
                "role": "assistant",
                "content": respuesta_completa
            }
        )

    except Exception as e:

        st.error(
            "😕 Ocurrió un inconveniente técnico "
            "al contactar con XISUS."
        )

        st.caption(
            f"Error detectado: {e}"
        )
