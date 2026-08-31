import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.write("Tu calvito de confianza 🤖")

modelo = st.sidebar.selectbox("🧠 Modelo", ["gemini-3.7-flash", "gemini-3.6-flash"])

pregunta = st.chat_input("Escribe tu pregunta...")

st.write("Modelo seleccionado:", modelo)

if pregunta: st.write("Pregunta recibida:", pregunta)

if pregunta: respuesta = cliente.models.generate_content(model=modelo, contents=pregunta)

if pregunta: st.write(respuesta.text)
