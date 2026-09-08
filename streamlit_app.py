import streamlit as st
from openai import OpenAI
import base64

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
# ==============================================================================
# 9. IMÁGENES: SUBIR O HACER UNA FOTO
# ==============================================================================

st.markdown("### 📷 Dale una imagen a XISUS")

col1, col2 = st.columns(2)

with col1:
    imagen_subida = st.file_uploader(
        "📁 Subir una imagen",
        type=["jpg", "jpeg", "png", "webp"],
        key="imagen_subida"
    )

with col2:
    imagen_camara = st.camera_input(
        "📸 Hacer una foto",
        key="imagen_camara"
    )

# Elegir qué imagen utilizar
imagen = imagen_camara if imagen_camara is not None else imagen_subida

# Mostrar la imagen seleccionada
if imagen is not None:

    st.image(
        imagen,
        caption="Imagen que verá XISUS",
        width=400
    )

# ==============================================================================
# 10. INPUT DEL CHAT
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

        # Si hay imagen, mostrarla también en el mensaje
        if imagen is not None:
            st.image(
                imagen,
                width=400
            )

    try:

        # ======================================================================
        # PREPARAR EL MENSAJE
        # ======================================================================

        if imagen is not None:

            # Convertir la imagen a Base64
            imagen_bytes = imagen.getvalue()

            imagen_base64 = base64.b64encode(
                imagen_bytes
            ).decode("utf-8")

            # Detectar el tipo MIME
            tipo_imagen = imagen.type

            # Crear Data URL
            imagen_data_url = (
                f"data:{tipo_imagen};base64,{imagen_base64}"
            )

            # Mensaje multimodal: texto + imagen
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

            # Mensaje normal de texto
            contenido_usuario = pregunta

        # ======================================================================
        # CREAR HISTORIAL PARA OPENAI
        # ======================================================================

        historial_limitado = st.session_state.historial[-16:]

        historial_para_openai = historial_limitado + [
            {
                "role": "user",
                "content": contenido_usuario
            }
        ]

        # ======================================================================
        # RESPUESTA DE XISUS
        # ======================================================================

        with st.chat_message("assistant"):

            stream = cliente.responses.create(
                model=modelo_visual,
                instructions=instrucciones[personalidad_visual],
                input=historial_para_openai,
                max_output_tokens=max_tokens,
                stream=True
            )

            respuesta_completa = ""

            placeholder = st.empty()

            for evento in stream:

                if evento.type == "response.output_text.delta":

                    respuesta_completa += evento.delta

                    placeholder.markdown(
                        respuesta_completa
                    )

        # ======================================================================
        # GUARDAR MENSAJE DEL USUARIO
        # ======================================================================

        st.session_state.historial.append({
            "role": "user",
            "content": pregunta
        })

        # ======================================================================
        # GUARDAR RESPUESTA DE XISUS
        # ======================================================================

        st.session_state.historial.append({
            "role": "assistant",
            "content": respuesta_completa
        })

    except Exception as e:

        st.error(
            "😕 Ocurrió un inconveniente técnico al "
            "analizar la imagen o generar la respuesta."
        )

        st.caption(
            f"Error detectado: {e}"
        )
