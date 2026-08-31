import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.write("Prueba de conexión")

pregunta = st.chat_input("Escribe Hola")

resultado = None
error = None

resultado = cliente.models.generate_content(model="gemini-2.5-flash", contents=pregunta) if pregunta else None

st.write(resultado.text if resultado else "Escribe una pregunta.")
