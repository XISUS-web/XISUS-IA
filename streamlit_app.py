import streamlit as st
from openai import OpenAI
import base64

# ==============================================================================
# 1. CONFIGURACIÓN
# ==============================================================================

st.set_page_config(
    page_title="XISUS IA",
    page_icon="👩‍🦲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ESTILO
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

div.stButton > button {
    border-radius: 8px;
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
# 3. OPENAI
# ==============================================================================

try:

    API_KEY = st.secrets["OPENAI_API_KEY"]

    cliente = OpenAI(
        api_key=API_KEY
    )

except Exception as e:

    st.error(
        "🔑 No se ha podido conectar con OpenAI."
    )

    st.caption(
        f"Error: {e}"
    )

    st.stop()

# ==============================================================================
# 4. MEMORIA
# ==============================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

if "imagen_actual" not in st.session_state:
    st.session_state.imagen_actual = None

# ==============================================================================
# 5. PERSONALIDADES
# ==============================================================================

instrucciones = {

    "Normal":
        "Eres XISUS, tu calvito de confianza. "
        "Eres útil, inteligente, claro y natural.",

    "Amigable":
        "Eres XISUS, un asistente extremadamente amigable, "
        "entusiasta y cálido. Hablas de forma natural y cercana.",

    "Profesional":
        "Eres XISUS, un asistente serio, profesional, "
        "preciso, formal y directo.",

    "Divertido":
        "Eres XISUS. Tienes mucho sentido del humor, "
        "haces bromas ligeras y eres divertido, "
        "pero siempre das respuestas útiles.",

    "Conciso":
        "Eres XISUS. Responde de forma extremadamente corta, "
        "clara y directa."
}

# ==============================================================================
# 6. BARRA LATERAL
# ==============================================================================

with st.sidebar:

    st.markdown(
        "<h2 style='text-align:center;'>⚙️ Panel de Control</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------------------------
    # MODELO
    # --------------------------------------------------------------------------

    st.subheader("🧠 Modelo")

    modelo_visual = st.selectbox(
        "Selecciona el cerebro:",
        [
            "gpt-5.6-luna",
            "gpt-5.6-terra",
            "gpt-5.6-sol"
        ],
        index=0
    )

    # --------------------------------------------------------------------------
    # PERSONALIDAD
    # --------------------------------------------------------------------------

    personalidad_visual = st.selectbox(
        "Personalidad:",
        [
            "Normal",
            "Amigable",
            "Profesional",
            "Divertido",
            "Conciso"
        ]
    )

    # --------------------------------------------------------------------------
    # LONGITUD
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("⚙️ Ajustes")

    max_tokens = st.slider(
        "Longitud máxima:",
        min_value=100,
        max_value=3000,
        value=1500,
        step=100
    )

    # --------------------------------------------------------------------------
    # IMÁGENES
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("📷 Imagen")

    modo_imagen = st.radio(
        "¿Quieres utilizar una imagen?",
        [
            "Ninguna",
            "📁 Subir imagen",
            "📸 Hacer foto"
        ],
        index=0
    )

    imagen_nueva = None

    if modo_imagen == "📁 Subir imagen":

        imagen_nueva = st.file_uploader(
            "Selecciona una imagen",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            key="uploader_imagen"
        )

    elif modo_imagen == "📸 Hacer foto":

        imagen_nueva = st.camera_input(
            "📸 Haz una foto",
            key="camara_imagen"
        )

    # Guardar imagen
    if imagen_nueva is not None:

        st.session_state.imagen_actual = imagen_nueva

    # Mostrar que hay una imagen guardada
    if st.session_state.imagen_actual is not None:

        st.success("🟢 Imagen preparada")

        if st.button(
            "🗑️ Quitar imagen",
            use_container_width=True
        ):

            st.session_state.imagen_actual = None

            st.rerun()

    # --------------------------------------------------------------------------
    # VOZ
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("🎙️ Voz")

    st.caption(
        "Graba un mensaje y XISUS lo convertirá en texto."
    )

    audio_usuario = st.audio_input(
        "🎙️ Grabar mensaje",
        sample_rate=16000,
        key="audio_usuario"
    )

    # --------------------------------------------------------------------------
    # LIMPIAR CHAT
    # --------------------------------------------------------------------------

    st.markdown("---")

    if st.button(
        "🗑️ Limpiar historial",
        use_container_width=True
    ):

        st.session_state.historial = []

        st.rerun()

    # --------------------------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------------------------

    st.markdown("---")

    st.subheader("💬 Estado")

    st.success(
        "🟢 OpenAI conectada"
    )

# ==============================================================================
# 7. CABECERA PRINCIPAL
# ==============================================================================

URL_DE_TU_IMAGEN = (
    "https://i.postimg.cc/Gmx2FfpG/IMG-2-20260818-WA0020.jpg"
)

st.image(
    URL_DE_TU_IMAGEN,
    width=200
)

st.markdown(
    """
    <h1 style="
        color:#ff4b4b;
        margin-top:10px;
        margin-bottom:0;
    ">
        👩‍🦲 XISUS IA
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        font-size:18px;
        color:#64748b;
    ">
        Tu asistente de inteligencia artificial de confianza.
    </p>
    """,
    unsafe_allow_html=True
)

st.write(
    "XISUS IA puede responder preguntas, mantener conversaciones, "
    "analizar imágenes y recibir mensajes mediante voz."
)

st.markdown("---")

# ==============================================================================
# 8. MOSTRAR IMAGEN ACTUAL
# ==============================================================================

imagen = st.session_state.imagen_actual

if imagen is not None:

    with st.expander("📷 Imagen preparada", expanded=True):

        st.image(
            imagen,
            width=400
        )

        st.caption(
            "XISUS utilizará esta imagen cuando envíes tu pregunta."
        )

# ==============================================================================
# 9. MOSTRAR HISTORIAL
# ==============================================================================

for mensaje in st.session_state.historial:

    with st.chat_message(
        mensaje["role"]
    ):

        st.markdown(
            mensaje["content"]
        )

# ==============================================================================
# 10. PROCESAR VOZ
# ==============================================================================

pregunta_voz = None

if audio_usuario is not None:

    try:

        with st.spinner(
            "🎙️ Transcribiendo tu voz..."
        ):

            transcripcion = cliente.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=(
                    "mensaje.wav",
                    audio_usuario.getvalue(),
                    "audio/wav"
                ),
                language="es"
            )

        pregunta_voz = transcripcion.text

        if pregunta_voz:

            st.info(
                f"🎙️ **Has dicho:** {pregunta_voz}"
            )

    except Exception as e:

        st.error(
            "❌ No se ha podido transcribir el audio."
        )

        st.caption(
            f"Error: {e}"
        )

# ==============================================================================
# 11. CHAT DE TEXTO
# ==============================================================================

pregunta_texto = st.chat_input(
    "Escribe tu consulta aquí para hablar con tu calvito..."
)

# ==============================================================================
# 12. ELEGIR TEXTO O VOZ
# ==============================================================================

if pregunta_voz:

    pregunta = pregunta_voz

else:

    pregunta = pregunta_texto

# ==============================================================================
# 13. PROCESAMIENTO DE XISUS
# ==============================================================================

if pregunta:

    # --------------------------------------------------------------------------
    # MOSTRAR PREGUNTA DEL USUARIO
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

            imagen_bytes = imagen.getvalue()

            imagen_base64 = base64.b64encode(
                imagen_bytes
            ).decode("utf-8")

            tipo_imagen = imagen.type

            imagen_data_url = (
                f"data:{tipo_imagen};base64,{imagen_base64}"
            )

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

            contenido_usuario = pregunta

        # ======================================================================
        # HISTORIAL
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
        # RESPUESTA
        # ======================================================================

        with st.chat_message("assistant"):

            respuesta_completa = ""

            placeholder = st.empty()

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
        # GUARDAR USUARIO
        # ======================================================================

        st.session_state.historial.append(
            {
                "role": "user",
                "content": pregunta
            }
        )

        # ======================================================================
        # GUARDAR XISUS
        # ======================================================================

        st.session_state.historial.append(
            {
                "role": "assistant",
                "content": respuesta_completa
            }
        )

        # ======================================================================
        # LIMPIAR IMAGEN DESPUÉS DE USARLA
        # ======================================================================

        if imagen is not None:

            st.session_state.imagen_actual = None

        # ======================================================================
        # RECARGAR
        # ======================================================================

        st.rerun()

    except Exception as e:

        st.error(
            "😕 XISUS ha tenido un problema al generar la respuesta."
        )

        st.caption(
            f"Error detectado: {e}"
        )
