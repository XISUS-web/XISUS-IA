import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.write("¡Bienvenido! Chatea con XISUS.")

pregunta = st.chat_input("De que quieres hablar hoy, tienes a tu calvito a disposicion")

respuesta = cliente.models.generate_content(model="gemini-flash-latest", contents=pregunta) if pregunta else None

st.write(respuesta.text if respuesta else "")
