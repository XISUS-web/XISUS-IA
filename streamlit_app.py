
import streamlit as st
from groq import Groq
from openai import OpenAI
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

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. CONEXIÓN CON GROQ Y OPENAI
# ==============================================================================

groq_disponible = False
openai_disponible = False

# -----------------------------
# GROQ — MOTOR PRINCIPAL
# -----------------------------

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

    cliente_groq = Groq(
        api_key=GROQ_API_KEY
    )

    groq_disponible = True

except Exception:
    cliente_groq = None


# -----------------------------
# OPENAI — MOTOR SECUNDARIO
# -----------------------------

try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    cliente_openai = OpenAI(
        api_key=OPENAI_API_KEY
    )

    openai_disponible = True

except Exception:
    cliente_openai = None


# Si ninguno está disponible, detener la aplicación

if not groq_disponible and not openai_disponible:

    st.error(
        "🔑 No hay ningún motor de IA disponible."
    )

    st.info(
        "Configura GROQ_API_KEY y/o OPENAI_API_KEY en los secrets de Streamlit."
    )

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

if "ultimo_motor" not in st.session_state:
    st.session_state.ultimo_motor = None


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
    # MOTORES
    # ==========================================================================

    st.subheader("⚡ Motores de IA")

    st.success(
        "🟢 Groq — MOTOR PRINCIPAL"
    )

    if openai_disponible:

        st.info(
            "🔵 OpenAI — MOTOR SECUNDARIO"
        )

    else:

        st.warning(
            "🔵 OpenAI — No configurado"
        )

    st.caption(
        "XISUS utiliza Groq primero. "
        "OpenAI entra automáticamente si Groq falla."
    )


    # ==========================================================================
    # MODELO GROQ
    # ==========================================================================

    st.markdown("---")

    st.subheader("🧠 Modelo Groq")

    modelo_groq = st.selectbox(
        "Selecciona el modelo principal:",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.6-27b"
        ],
        index=0
    )


    # ==========================================================================
    # MODELO OPENAI
    # ==========================================================================

    st.subheader("🔵 Modelo OpenAI")

    modelo_openai = st.selectbox(
        "Modelo secundario:",
        [
            "gpt-5-mini",
            "gpt-5",
            "gpt-5-nano"
        ],
        index=0
    )


    # ==========================================================================
    # PERSONALIDAD
    # ==========================================================================

    st.markdown("---")

    st.subheader("🎭 Personalidad")

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


    if imagen_nueva is not None:

        contenido_imagen = imagen_nueva.getvalue()

        if contenido_imagen:

            st.session_state.imagen_actual = contenido_imagen


    if st.session_state.imagen_actual is not None:

        st.success(
            "🟢 Imagen preparada"
        )

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

        st.session_state.ultimo_motor = None

        st.rerun()


    # ==========================================================================
    # ESTADO
    # ==========================================================================

    st.markdown("---")

    st.subheader("💬 Estado")

    if groq_disponible:

        st.success(
            "🟢 Groq disponible"
        )

    else:

        st.error(
            "🔴 Groq no disponible"
        )

    if openai_disponible:

        st.info(
            "🔵 OpenAI disponible"
        )

    else:

        st.warning(
            "🟠 OpenAI no disponible"
        )


# ==============================================================================
# 7. CABECERA
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
# 8. IMAGEN PREPARADA
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
# 9. HISTORIAL
# ==============================================================================

for mensaje in st.session_state.historial:

    with st.chat_message(
        mensaje["role"]
    ):

        st.markdown(
            mensaje["content"]
        )


# ==============================================================================
# 10. VOZ → TEXTO
# ==============================================================================

pregunta_voz = None

if audio_usuario is not None:

    audio_bytes = audio_usuario.getvalue()

    audio_hash = hashlib.md5(
        audio_bytes
    ).hexdigest()

    if (
        st.session_state.audio_procesado
        != audio_hash
    ):

        # La transcripción utiliza Groq como principal.

        if groq_disponible:

            try:

                with st.spinner(
                    "🎙️ XISUS está escuchando con Groq..."
                ):

                    transcripcion = (
                        cliente_groq.audio.transcriptions.create(
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

            except Exception as e:

                st.warning(
                    "⚠️ Groq no pudo procesar la voz."
                )

                # Intentar OpenAI como respaldo

                if openai_disponible:

                    try:

                        with st.spinner(
                            "🔵 Intentando transcripción con OpenAI..."
                        ):

                            archivo_audio = (
                                "mensaje.wav",
                                audio_bytes
                            )

                            transcripcion = (
                                cliente_openai.audio.transcriptions.create(
                                    model="whisper-1",
                                    file=archivo_audio
                                )
                            )

                        pregunta_voz = transcripcion.text.strip()

                        st.session_state.audio_procesado = audio_hash

                    except Exception as e2:

                        st.error(
                            "❌ Ningún motor pudo transcribir el audio."
                        )

                        st.caption(
                            f"Groq: {e}"
                        )

                        st.caption(
                            f"OpenAI: {e2}"
                        )

        elif openai_disponible:

            try:

                with st.spinner(
                    "🔵 Transcribiendo con OpenAI..."
                ):

                    transcripcion = (
                        cliente_openai.audio.transcriptions.create(
                            model="whisper-1",
                            file=(
                                "mensaje.wav",
                                audio_bytes
                            )
                        )
                    )

                pregunta_voz = transcripcion.text.strip()

                st.session_state.audio_procesado = audio_hash

            except Exception as e:

                st.error(
                    "❌ No se ha podido transcribir el audio."
                )

                st.caption(
                    f"Error: {e}"
                )


        if pregunta_voz:

            st.info(
                f"🎙️ **Has dicho:** {pregunta_voz}"
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
# 13. FUNCIÓN PARA CONSTRUIR IMAGEN
# ==============================================================================

def crear_contenido_con_imagen(pregunta, imagen):

    imagen_base64 = base64.b64encode(
        imagen
    ).decode("utf-8")


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


    return [

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


# ==============================================================================
# 14. PROCESAMIENTO PRINCIPAL
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


    # --------------------------------------------------------------------------
    # CONSTRUIR HISTORIAL PARA LA IA
    # --------------------------------------------------------------------------

    mensajes = [

        {
            "role": "system",
            "content": instrucciones[
                personalidad_visual
            ]
        }

    ]


    for mensaje in st.session_state.historial[-16:]:

        mensajes.append(
            {
                "role": mensaje["role"],
                "content": mensaje["content"]
            }
        )


    # --------------------------------------------------------------------------
    # MENSAJE ACTUAL
    # --------------------------------------------------------------------------

    if imagen is not None:

        contenido_usuario = crear_contenido_con_imagen(
            pregunta,
            imagen
        )

    else:

        contenido_usuario = pregunta


    mensajes.append(
        {
            "role": "user",
            "content": contenido_usuario
        }
    )


    # ==========================================================================
    # 15. GROQ — MOTOR PRINCIPAL
    # ==========================================================================

    respuesta_completa = ""

    respuesta_generada = False

    error_groq = None


    if groq_disponible:

        try:

            with st.chat_message("assistant"):

                placeholder = st.empty()

                placeholder.caption(
                    "🟢 XISUS está pensando con Groq..."
                )


                # Si hay imagen usamos el modelo multimodal.
                # Si no hay imagen utilizamos el modelo elegido.

                if imagen is not None:

                    modelo_final_groq = "qwen/qwen3.6-27b"

                else:

                    modelo_final_groq = modelo_groq


                stream = cliente_groq.chat.completions.create(

                    model=modelo_final_groq,

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


                if respuesta_completa.strip():

                    respuesta_generada = True

                    st.session_state.ultimo_motor = "Groq"


        except Exception as e:

            error_groq = e

            respuesta_completa = ""


    # ==========================================================================
    # 16. OPENAI — MOTOR SECUNDARIO
    # ==========================================================================

    if not respuesta_generada:

        if openai_disponible:

            try:

                with st.chat_message("assistant"):

                    placeholder = st.empty()

                    placeholder.caption(
                        "🔵 Groq no respondió. XISUS está usando OpenAI..."
                    )


                    # OpenAI recibe el mismo historial.

                    stream_openai = (
                        cliente_openai.chat.completions.create(

                            model=modelo_openai,

                            messages=mensajes,

                            temperature=temperatura,

                            max_completion_tokens=max_tokens,

                            stream=True

                        )
                    )


                    for chunk in stream_openai:

                        if not chunk.choices:

                            continue

                        delta = chunk.choices[0].delta

                        if delta.content:

                            respuesta_completa += delta.content

                            placeholder.markdown(
                                respuesta_completa
                            )


                    if respuesta_completa.strip():

                        respuesta_generada = True

                        st.session_state.ultimo_motor = (
                            "OpenAI (respaldo)"
                        )


            except Exception as e:

                if error_groq:

                    st.error(
                        "❌ Groq y OpenAI han fallado."
                    )

                    st.caption(
                        f"Error Groq: {error_groq}"
                    )

                    st.caption(
                        f"Error OpenAI: {e}"
                    )

                else:

                    st.error(
                        "❌ OpenAI no ha podido generar la respuesta."
                    )

                    st.caption(
                        f"Error: {e}"
                    )


        else:

            if error_groq:

                st.error(
                    "❌ Groq ha fallado y OpenAI no está configurado."
                )

                st.caption(
                    f"Error Groq: {error_groq}"
                )


    # ==========================================================================
    # 17. GUARDAR CONVERSACIÓN
    # ==========================================================================

    if respuesta_generada:

        st.session_state.historial.append(
            {
                "role": "user",
                "content": pregunta
            }
        )


        st.session_state.historial.append(
            {
                "role": "assistant",
                "content": respuesta_completa
            }
        )


        # ----------------------------------------------------------------------
        # MOSTRAR MOTOR UTILIZADO
        # ----------------------------------------------------------------------

        if st.session_state.ultimo_motor == "Groq":

            st.caption(
                "🟢 Motor utilizado: Groq — principal"
            )

        elif (
            st.session_state.ultimo_motor
            == "OpenAI (respaldo)"
        ):

            st.caption(
                "🔵 Motor utilizado: OpenAI — secundario"
            )


        # ----------------------------------------------------------------------
        # LIMPIAR IMAGEN
        # ----------------------------------------------------------------------

        if imagen is not None:

            st.session_state.imagen_actual = None


        # ----------------------------------------------------------------------
        # RECARGAR
        # ----------------------------------------------------------------------

        st.rerun()
