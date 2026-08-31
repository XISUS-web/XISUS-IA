import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

st.sidebar.title("⚙️ Configuración")

modelo = st.sidebar.selectbox(
"🧠 Modelo Gemini",
[
"gemini-3.7-flash",
"gemini-3.6-flash",
"gemini-3.5-flash",
"gemini-3.5-flash-lite",
"gemini-3.1-flash-lite"
]
)

st.sidebar.markdown("---")
st.sidebar.write("Modelo seleccionado:")
st.sidebar.code(modelo)

pregunta = st.chat_input("¿De qué quieres hablar hoy? 😎")

respuesta = cliente.models.generate_content(model=modelo, contents=pregunta) if pregunta else None

st.write(respuesta.text if respuesta else "👋 Escribe una pregunta para comenzar.")
