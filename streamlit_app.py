import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.write("Prueba de conexión con Gemini")

pregunta = st.chat_input("Escribe una pregunta")

if pregunta:
st.write("Pregunta recibida:", pregunta)
try:
respuesta = cliente.models.generate_content(
model="gemini-2.5-flash",
contents=pregunta
)
st.write(respuesta.text)
except Exception as e:
st.error("Gemini ha devuelto un error")
st.write("Tipo:", type(e).**name**)
st.write("Código:", getattr(e, "status_code", "No disponible"))
st.write("Mensaje:", str(e))
