import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

API_KEY = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=API_KEY)

st.title("👩‍🦲 XISUS")
st.write("Prueba directa de Gemini 3.7 Flash")

pregunta = st.chat_input("Escribe algo...")

if pregunta: respuesta = cliente.models.generate_content(model="gemini-3.7-flash", contents=pregunta)

if pregunta: st.write(respuesta.text)
