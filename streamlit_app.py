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
"gemini-3.6-flash",
"gemini-3.7-flash",
"gemini-3.5-flash"
]
)

temperatura = st.sidebar.slider("🌡️ Creatividad", 0.0, 2.0, 0.7, 0.1)

pregunta = st.chat_input("¿De qué quieres hablar hoy? 😎")

respuesta = cliente.models.generate_content(
model=modelo,
contents=pregunta
) if pregunta else None

st.write(respuesta.text if respuesta else "👋 ¡Hola! Escribe algo para comenzar.")

