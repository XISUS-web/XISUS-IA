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
"gemini-3.5-flash"
]
)



pregunta = st.chat_input("¿De qué quieres hablar hoy? 😎")

respuesta = None

if pregunta:
try:
respuesta = cliente.models.generate_content(
model=modelo,
contents=pregunta
)
st.write(respuesta.text)
except Exception as error:
st.error("❌ Gemini ha dado un error")
st.write("Tipo de error:", type(error).name)
st.write("Código:", getattr(error, "status_code", "No disponible"))
st.write("Detalles:", str(error))

st.write(respuesta.text if respuesta else "👋 ¡Hola! Escribe algo para comenzar.")

