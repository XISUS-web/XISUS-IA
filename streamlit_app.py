import streamlit as st
from google import genai
from google.genai import types

# ============================================================

# XISUS 2.0

# Asistente IA con Gemini + Streamlit

# ============================================================

st.set_page_config(
page_title="XISUS",
page_icon="👩‍🦲",
layout="centered"
)

# ============================================================

# ESTILOS

# ============================================================

st.markdown("""

<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #FF4B4B;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #888888;
        font-size: 17px;
        margin-top: 0;
        margin-bottom: 25px;
    }

    .model-box {
        background: linear-gradient(135deg, #ff4b4b22, #ff4b4b08);
        border: 1px solid #ff4b4b55;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 15px;
    }

    .status-ok {
        color: #21c354;
        font-weight: bold;
    }

    .footer {
        text-align: center;
        color: #888888;
        font-size: 13px;
        margin-top: 40px;
    }
</style>

""", unsafe_allow_html=True)

# ============================================================

# API

# ============================================================

LLAVE_API = st.secrets["GEMINI_API_KEY"]

if "client" not in st.session_state:
st.session_state.client = genai.Client(api_key=LLAVE_API)

# ============================================================

# CONFIGURACIÓN INICIAL

# ============================================================

if "modelo" not in st.session_state:
st.session_state.modelo = "gemini-3.7-flash"

if "historial" not in st.session_state:
st.session_state.historial = []

if "chat" not in st.session_state:
st.session_state.chat = st.session_state.client.chats.create(
model=st.session_state.modelo
)

if "modelos_disponibles" not in st.session_state:
st.session_state.modelos_disponibles = []

if "memoria" not in st.session_state:
st.session_state.memoria = True

if "temperatura" not in st.session_state:
st.session_state.temperatura = 0.7

if "max_tokens" not in st.session_state:
st.session_state.max_tokens = 2048

# ============================================================

# FUNCIONES

# ============================================================

def obtener_modelos():
modelos = []

```
try:
    for modelo in st.session_state.client.models.list():
        acciones = getattr(modelo, "supported_actions", []) or []
        nombre = getattr(modelo, "name", "")

        if "generateContent" in acciones and nombre:
            nombre = nombre.replace("models/", "")
            modelos.append(nombre)

    return modelos

except Exception:
    return []
```

def crear_chat():
st.session_state.chat = st.session_state.client.chats.create(
model=st.session_state.modelo
)

def mensaje_error(error):
codigo = getattr(error, "status_code", None)
texto = str(error)

```
if codigo == 400:
    return "⚠️ Gemini no ha podido procesar la petición. Prueba a reformular la pregunta."

if codigo == 403:
    return "🔐 Gemini ha rechazado el acceso. Comprueba los permisos de tu API key o del proyecto."

if codigo == 404:
    return (
        "🔎 El modelo seleccionado no está disponible para tu cuenta. "
        "Ve a ⚙️ Configuración y selecciona otro modelo."
    )

if codigo == 429:
    return (
        "⏳ Has alcanzado temporalmente el límite de uso de Gemini. "
        "Espera un poco o prueba otro modelo."
    )

if codigo in [500, 502, 503, 504]:
    return (
        "☁️ Gemini está teniendo problemas temporales. "
        "Espera unos segundos y vuelve a intentarlo."
    )

if "quota" in texto.lower():
    return "⏳ Se ha alcanzado el límite de uso de la API."

if "not found" in texto.lower():
    return "🔎 El modelo seleccionado no está disponible."

return (
    "😕 XISUS no ha podido obtener una respuesta de Gemini. "
    "Prueba de nuevo o cambia de modelo."
)
```

def cambiar_modelo(nuevo_modelo):
st.session_state.modelo = nuevo_modelo
st.session_state.historial = []
crear_chat()

# ============================================================

# SIDEBAR

# ============================================================

with st.sidebar:

```
st.title("⚙️ Configuración")
st.markdown("---")

st.subheader("🧠 Modelo Gemini")

modelos_fijos = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite"
]

modelos = st.session_state.modelos_disponibles

lista_modelos = list(dict.fromkeys(modelos_fijos + modelos))

modelo_actual = st.session_state.modelo

if modelo_actual not in lista_modelos:
    lista_modelos.insert(0, modelo_actual)

nuevo_modelo = st.selectbox(
    "Selecciona el modelo:",
    lista_modelos,
    index=lista_modelos.index(modelo_actual)
)

if nuevo_modelo != st.session_state.modelo:
    cambiar_modelo(nuevo_modelo)
    st.rerun()

st.markdown(
    f"""
    <div class="model-box">
    🤖 <b>Modelo activo</b><br>
    <code>{st.session_state.modelo}</code>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button(
    "🔍 Detectar modelos disponibles",
    use_container_width=True
):
    with st.spinner("Consultando Gemini..."):
        encontrados = obtener_modelos()

    if encontrados:
        st.session_state.modelos_disponibles = encontrados
        st.success(f"Encontrados {len(encontrados)} modelos.")
        st.rerun()
    else:
        st.warning(
            "No se han podido obtener los modelos disponibles."
        )

st.markdown("---")

st.subheader("🧠 Memoria")

st.session_state.memoria = st.toggle(
    "Mantener contexto de conversación",
    value=st.session_state.memoria
)

st.caption(
    "Si está activada, XISUS recuerda los mensajes anteriores "
    "durante esta sesión."
)

st.markdown("---")

st.subheader("🎛️ Respuestas")

st.session_state.temperatura = st.slider(
    "Creatividad",
    min_value=0.0,
    max_value=2.0,
    value=st.session_state.temperatura,
    step=0.1
)

st.session_state.max_tokens = st.slider(
    "Longitud máxima",
    min_value=256,
    max_value=8192,
    value=st.session_state.max_tokens,
    step=256
)

st.markdown("---")

st.subheader("🧹 Conversación")

if st.button(
    "🗑️ Borrar historial",
    use_container_width=True
):
    st.session_state.historial = []
    crear_chat()
    st.rerun()

if st.button(
    "🔄 Reiniciar XISUS",
    use_container_width=True
):
    st.session_state.historial = []
    crear_chat()
    st.rerun()

st.markdown("---")

st.subheader("👨‍💻 Desarrollador")
st.info("Creado con orgullo por **Ernesto** 🚀")
```

# ============================================================

# CABECERA

# ============================================================

st.markdown(
'<div class="main-title">👩‍🦲 XISUS</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Tu calvito de confianza impulsado por Gemini 🤖</div>',
unsafe_allow_html=True
)

# ============================================================

# INFORMACIÓN DEL MODELO

# ============================================================

st.caption(
f"🟢 XISUS está utilizando `{st.session_state.modelo}`"
)

st.markdown("---")

# ============================================================

# HISTORIAL

# ============================================================

for mensaje in st.session_state.historial:

```
with st.chat_message(mensaje["rol"]):
    st.markdown(mensaje["texto"])
```

# ============================================================

# CHAT

# ============================================================

pregunta = st.chat_input(
"¿De qué quieres hablar hoy? Tienes a tu calvito a disposición 😎"
)

if pregunta:

```
with st.chat_message("user"):
    st.markdown(pregunta)

st.session_state.historial.append(
    {
        "rol": "user",
        "texto": pregunta
    }
)

with st.chat_message("assistant"):

    with st.spinner("🧠 XISUS está pensando..."):

        try:

            configuracion = types.GenerateContentConfig(
                temperature=st.session_state.temperatura,
                max_output_tokens=st.session_state.max_tokens
            )

            if st.session_state.memoria:

                respuesta = st.session_state.chat.send_message(
                    pregunta,
                    config=configuracion
                )

            else:

                respuesta = st.session_state.client.models.generate_content(
                    model=st.session_state.modelo,
                    contents=pregunta,
                    config=configuracion
                )

            texto_respuesta = respuesta.text

            if not texto_respuesta:
                texto_respuesta = (
                    "🤔 Gemini no ha devuelto texto en esta ocasión. "
                    "Prueba de nuevo."
                )

            st.markdown(texto_respuesta)

            st.session_state.historial.append(
                {
                    "rol": "assistant",
                    "texto": texto_respuesta
                }
            )

        except Exception as e:

            st.error(mensaje_error(e))

            st.caption(
                f"Modelo utilizado: `{st.session_state.modelo}`"
            )
```

# ============================================================

# PIE

# ============================================================

st.markdown(
""" <div class="footer">
XISUS 2.0 · Powered by Google Gemini 🚀 </div>
""",
unsafe_allow_html=True
)
