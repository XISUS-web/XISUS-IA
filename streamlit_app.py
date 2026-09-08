```python
import streamlit as st
from groq import Groq
import base64
import hashlib

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

[data-testid="stChatMessage"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. CONEXIÓN CON GROQ
# ==============================================================================

try:

    API_KEY = st.secrets["GROQ_API_KEY"]

    cliente = Groq(
        api_key=API_KEY
    )

except Exception as e:

    st.error("🔑 No se ha podido conectar con Groq.")

    st.caption(f"Error: {e}")

    st.stop()


# ==============================================================================
# 4. MEMORIA
# ==============================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

if "imagen_actual" not in st.session_state:
    st.session_state.imagen_actual = None

if "audio_procesado" not in st.session_state:
    st.session_state.audio_procesado = None


# ==============================================================================
# 5. PERSONALIDADES
# ==============================================================================

instrucciones = {

    "Normal":
        """
        Eres XISUS, el calvito de confianza del usuario.
        Eres útil, inteligente, claro y natural.
        Responde siempre en español salvo que el usuario pida otro idioma.
        """,

    "Amigable":
        """
        Eres XISUS, un asistente extremadamente amigable,
        entusiasta y cercano.
        Hablas de forma natural y cálida.
        Responde siempre en español salvo que el usuario pida otro idioma.
        """,

    "Profesional":
        """
        Eres XISUS, un asistente serio, profesional,
        preciso, formal y directo.
        Responde siempre en español salvo que el usuario pida otro idioma.
        """,

    "Divertido":
        """
        Eres XISUS.
        Tienes mucho sentido del humor y haces bromas ligeras,
        pero siempre proporcionas respuestas útiles.
        Responde siempre en español salvo que el usuario pida otro idioma.
        """,

    "Conciso":
        """
        Eres XISUS.
        Responde de forma extremadamente corta,
        clara y directa.
        Responde siempre en español salvo que el usuario pida otro idioma.
        """
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

    # ==========================================================================
    # MODELO
    # ==========================================================================

    st.subheader("🧠 Modelo")

    modelo_visual = st.selectbox(
        "Selecciona el cerebro:",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.6-27b"
        ],
        index=0
    )

    st.caption(
        "Qwen 3.6 permite analizar imágenes."
    )


    # ==========================================================================
    # PERSONALIDAD
    # ==========================================================================

    personalidad_visual = st.selectbox(
        "Personalidad:",
        [
            "Normal",
            "Amigable",
            "Profesional",
            "Divertido",
            "Conciso"
        ],
        index=0
    )


    # ==========================================================================
    # AJUSTES
    # ==========================================================================

    st.markdown("---")

    st.subheader("⚙️ Ajustes")

    max_tokens = st.slider(
        "Longitud máxima:",
        min_value=100,
        max_value=3000,
        value=1200,
        step=100
    )

    temperatura = st.slider(
        "Creatividad:",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )


    # ==========================================================================
    # IMÁGENES
    # ==========================================================================

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


    # --------------------------------------------------------------------------
    # SUBIR IMAGEN
    # --------------------------------------------------------------------------

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


    # --------------------------------------------------------------------------
    # CÁMARA
    # --------------------------------------------------------------------------

    elif modo_imagen == "📸 Hacer foto":

        imagen_nueva = st.camera_input(
            "📸 Haz una foto",
            key="camara_imagen"
        )


    # --------------------------------------------------------------------------
    # GUARDAR IMAGEN
    # --------------------------------------------------------------------------

    if imagen_nueva is not None:

        nuevo_contenido = imagen_nueva.getvalue()

        if nuevo_contenido:

            st.session_state.imagen_actual = nuevo_contenido


    # --------------------------------------------------------------------------
    # MOSTRAR IMAGEN PREPARADA
    # --------------------------------------------------------------------------

    if st.session_state.imagen_actual is not None:

        st.success("🟢 Imagen preparada")

        st.image(
            st.session_state.imagen_actual,
            width=250
        )

        if st.button(
            "🗑️ Quitar imagen",
            use_container_width=True
        ):

            st.session_state.imagen_actual = None

            st.rerun()


    # ==========================================================================
    # VOZ
    # ==========================================================================

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


    # ==========================================================================
    # LIMPIAR CHAT
    # ==========================================================================

    st.markdown("---")

    if st.button(
        "🗑️ Limpiar historial",
        use_container_width=True
    ):

        st.session_state.historial = []

        st.session_state.imagen_actual = None

        st.session_state.audio_procesado = None

        st.rerun()


    # ==========================================================================
    # ESTADO
    # ==========================================================================

    st.markdown("---")

    st.subheader("💬 Estado")

    st.success(
        "🟢 Groq conectada"
    )


# ==============================================================================
# 7. CABECERA PRINCIPAL
# ==============================================================================

URL_DE_TU_IMAGEN = (
    "https://i.postimg.cc/Gmx2FfpG/IMG-2-20260818-WA0020.jpg"
)

try:

    st.image(
        URL_DE_TU_IMAGEN,
        width=200
    )

except Exception:

    pass


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
# 8. MOSTRAR IMAGEN PREPARADA
# ==============================================================================

imagen = st.session_state.imagen_actual

if imagen is not None:

    with st.expander(
        "📷 Imagen preparada para XISUS",
        expanded=True
    ):

        st.image(
            imagen,
            width=400
        )

        st.caption(
            "La imagen se enviará cuando hagas una pregunta."
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
# 10. TRANSCRIPCIÓN DE VOZ
# ==============================================================================

pregunta_voz = None

if audio_usuario is not None:

    audio_bytes = audio_usuario.getvalue()

    audio_hash = hashlib.md5(
        audio_bytes
    ).hexdigest()


    # Evitar procesar el mismo audio varias veces

    if (
        st.session_state.audio_procesado
        != audio_hash
    ):

        try:

            with st.spinner(
                "🎙️ XISUS está escuchando..."
            ):

                transcripcion = (
                    cliente.audio.transcriptions.create(
                        file=(
                            "mensaje.wav",
                            audio_bytes,
                            "audio/wav"
                        ),
                        model="whisper-large-v3-turbo",
                        language="es",
                        temperature=0
                    )
                )

            pregunta_voz = transcripcion.text.strip()

            st.session_state.audio_procesado = audio_hash

            if pregunta_voz:

                st.info(
                    f"🎙️ **Has dicho:** {pregunta_voz}"
                )

        except Exception as e:

            st.error(
                "❌ No se ha podido transcribir el audio."
            )

            st.caption(
                f"Error de voz: {e}"
            )


# ==============================================================================
# 11. CHAT DE TEXTO
# ==============================================================================

pregunta_texto = st.chat_input(
    "Escribe tu consulta aquí para hablar con tu calvito..."
)


# ==============================================================================
# 12. ELEGIR PREGUNTA
# ==============================================================================

if pregunta_voz:

    pregunta = pregunta_voz

else:

    pregunta = pregunta_texto


# ==============================================================================
# 13. PROCESAMIENTO DE XISUS
# ==============================================================================

if pregunta:

    # ==========================================================================
    # MOSTRAR MENSAJE DEL USUARIO
    # ==========================================================================

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
        # CONSTRUIR MENSAJES
        # ======================================================================

        mensajes = [

            {
                "role": "system",
                "content": instrucciones[
                    personalidad_visual
                ]
            }

        ]


        # ======================================================================
        # HISTORIAL
        # ======================================================================

        for mensaje in st.session_state.historial[-16:]:

            mensajes.append(
                {
                    "role": mensaje["role"],
                    "content": mensaje["content"]
                }
            )


        # ======================================================================
        # MENSAJE ACTUAL
        # ======================================================================

        if imagen is not None:

            imagen_base64 = base64.b64encode(
                imagen
            ).decode("utf-8")


            # Detectar formato

            if imagen.startswith(b"\x89PNG"):

                tipo_imagen = "image/png"

            elif imagen.startswith(b"RIFF"):

                tipo_imagen = "image/webp"

            elif imagen.startswith(b"\xff\xd8"):

                tipo_imagen = "image/jpeg"

            else:

                tipo_imagen = "image/jpeg"


            imagen_data_url = (
                f"data:{tipo_imagen};base64,"
                f"{imagen_base64}"
            )


            contenido_usuario = [

                {
                    "type": "text",
                    "text": pregunta
                },

                {
                    "type": "image_url",
                    "image_url": {
                        "url": imagen_data_url
                    }
                }

            ]

        else:

            contenido_usuario = pregunta


        # ======================================================================
        # AÑADIR MENSAJE ACTUAL
        # ======================================================================

        mensajes.append(
            {
                "role": "user",
                "content": contenido_usuario
            }
        )


        # ======================================================================
        # SELECCIONAR MODELO
        # ======================================================================

        if imagen is not None:

            # Modelo multimodal actual de Groq
            modelo_final = "qwen/qwen3.6-27b"

        else:

            modelo_final = modelo_visual


        # ======================================================================
        # GENERAR RESPUESTA
        # ======================================================================

        with st.chat_message("assistant"):

            respuesta_completa = ""

            placeholder = st.empty()


            stream = cliente.chat.completions.create(

                model=modelo_final,

                messages=mensajes,

                temperature=temperatura,

                max_completion_tokens=max_tokens,

                stream=True

            )


            for chunk in stream:

                if not chunk.choices:

                    continue

                delta = chunk.choices[0].delta

                if delta.content:

                    respuesta_completa += delta.content

                    placeholder.markdown(
                        respuesta_completa
                    )


        # ======================================================================
        # GUARDAR MENSAJE DEL USUARIO
        # ======================================================================

        st.session_state.historial.append(
            {
                "role": "user",
                "content": pregunta
            }
        )


        # ======================================================================
        # GUARDAR RESPUESTA DE XISUS
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
```
