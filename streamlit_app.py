import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]

st.title("👩‍🦲 XISUS - Prueba Gemini")

st.write("🔑 API Key encontrada:", bool(LLAVE_API))

cliente = genai.Client(api_key=LLAVE_API)

st.write("🤖 Probando conexión con Gemini...")

resultado = cliente.models.list()

st.success("✅ Conexión con Gemini realizada correctamente")

st.write("Modelos disponibles para tu API Key:")

for modelo in resultado:
 st.write(modelo.name)
