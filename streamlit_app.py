import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲", layout="centered")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

if "historial" not in st.session_state:
st.session_state.historial = []

if "modelo" not in st.session_state:
st.session_state.modelo = "gemini-3.6-flash"

st.markdown("""

<style>
.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #FF4B4B;
    margin-bottom: 0;
}
.subtitle {
    text-align: center;
    color: #888888;
    font-size: 17px;
    margin-bottom: 25px;
}
.model-box {
    background: #ff4b4b18;
    border: 1px solid #ff4b4b55;
    border-radius: 12px;
    padding: 12px;
}
</style>

""", unsafe_allow_html=True)

st.markdown(
'<div class="main-title">👩‍🦲 XISUS</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Tu calvito de confianza impulsado por Gemini 🤖</div>',
unsafe_allow_html=True
)

st.markdown("---")

modelos = [
"gemini-3.6-flash",
"gemini-3.7-flash",
"gemini-3.5-flash",
"gemini-3.5-flash-lite",
"gemini-3.1-flash-lite"
]

with st.sidebar:
st.title("⚙️ Configuración")
st.markdown("---")

```
nuevo_modelo = st.selectbox(
    "🧠 Modelo Gemini",
    modelos,
    index=modelos.index(st.session_state.modelo)
)

if nuevo_modelo != st.session_state.modelo:
    st.session_state.modelo = nuevo_modelo
    st.session_state.historial = []
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

st.markdown("---")

temperatura = st.slider(
    "🌡️ Creatividad",
    0.0,
    2.0,
    0.7,
    0.1
)

max_tokens = st.slider(
    "📏 Longitud máxima",
    256,
    8192,
    2048,
    256
)

st.markdown("---")

if st.button("🗑️ Borrar historial", use_container_width=True):
    st.session_state.historial = []
    st.rerun()

st.markdown("---")

st.info("Creado con orgullo por **Ernesto** 🚀")
```

st.caption(
f"🟢 Modelo activo: `{st.session_state.modelo}`"
)

for mensaje in st.session_state.historial:
with st.chat_message(mensaje["rol"]):
st.markdown(mensaje["texto"])

pregunta = st.chat_input(
"¿De qué quieres hablar hoy? Tienes a tu calvito a disposición 😎"
)

if pregunta:
st.session_state.historial.append(
{
"rol": "user",
"texto": pregunta
}
)

```
with st.chat_message("user"):
    st.markdown(pregunta)

with st.chat_message("assistant"):
    with st.spinner("🧠 XISUS está pensando..."):
        try:
            configuracion = types.GenerateContentConfig(
                temperature=temperatura,
                max_output_tokens=max_tokens
            )

            respuesta = cliente.models.generate_content(
                model=st.session_state.modelo,
                contents=pregunta,
                config=configuracion
            )

            texto = respuesta.text

            if not texto:
                texto = "🤔 Gemini no ha devuelto ninguna respuesta."

            st.markdown(texto)

            st.session_state.historial.append(
                {
                    "rol": "assistant",
                    "texto": texto
                }
            )

        except Exception as e:
            codigo = getattr(e, "status_code", None)

            if codigo == 404:
                mensaje_error = "🔎 El modelo seleccionado no está disponible para tu cuenta. Prueba otro desde ⚙️ Configuración."

            elif codigo == 403:
                mensaje_error = "🔐 Gemini ha rechazado el acceso. Comprueba tu API key y los permisos del proyecto."

            elif codigo == 429:
                mensaje_error = "⏳ Has alcanzado el límite de uso de Gemini. Espera un poco y vuelve a intentarlo."

            elif codigo in [500, 502, 503, 504]:
                mensaje_error = "☁️ Gemini está teniendo problemas temporales. Espera unos segundos y vuelve a intentarlo."

            else:
                mensaje_error = "😕 XISUS no ha podido comunicarse con Gemini. Prueba de nuevo."

            st.warning(mensaje_error)
```

st.markdown("---")

st.markdown(
'<p style="text-align:center;color:#888;font-size:13px;">XISUS 2.0 · Powered by Gemini 🚀</p>',
unsafe_allow_html=True
)
