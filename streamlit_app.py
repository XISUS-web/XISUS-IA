import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲", layout="centered")

LLAVE_API = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.write("¡Bienvenido! Chatea con XISUS.")

pregunta = st.chat_input("De que quieres hablar hoy, tienes a tu calvito a disposicion")

if pregunta:
st.chat_message("user").write(pregunta)
try:
respuesta = cliente.models.generate_content(
model="gemini-2.5-flash",
contents=pregunta
)
st.chat_message("assistant").write(respuesta.text)
except Exception as e:
st.error(f"Error de Gemini: {type(e).**name**}")
st.code(str(e))
