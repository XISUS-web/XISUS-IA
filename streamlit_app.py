import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲", layout="centered")

LLAVE_API = st.secrets["GEMINI_API_KEY"]

if "client" not in st.session_state: st.session_state.client = genai.Client(api_key=LLAVE_API)
if "chat" not in st.session_state: st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
if "historial" not in st.session_state: st.session_state.historial = []

with st.sidebar:
st.title("⚙️ Configuración")
st.markdown("---")
st.subheader("Desarrollador:")
st.info("Creado con orgullo por **Ernesto** 🚀")

```
if st.button("🗑️ Limpiar Historial", use_container_width=True):
    st.session_state.historial = []
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
    st.rerun()
```

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>👩‍🦲 Chatea libremente con XISUS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>¡Bienvenido! Chatea con XISUS.</p>", unsafe_allow_html=True)
st.markdown("---")

for mensaje in st.session_state.historial:
with st.chat_message(mensaje["rol"]):
st.markdown(mensaje["texto"])

if pregunta := st.chat_input("De que quieres hablar hoy, tienes a tu calvito a disposicion"):
st.session_state.historial.append({"rol": "user", "texto": pregunta})

```
with st.chat_message("user"):
    st.markdown(pregunta)

with st.chat_message("assistant"):
    with st.spinner("XISUS está pensando..."):
        try:
            respuesta = st.session_state.chat.send_message(pregunta)
            texto = respuesta.text
            st.markdown(texto)
            st.session_state.historial.append({"rol": "assistant", "texto": texto})
        except Exception as e:
            st.error(f"Error de Gemini: {type(e).__name__}")
            st.code(str(e))
```
