import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

API_KEY = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=API_KEY)

st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

pregunta = st.chat_input("Escribe algo...")

resultado = cliente.models.generate_content(model="gemini-3.5-flash", contents=pregunta) if pregunta else None

st.chat_message("user").write(pregunta) if pregunta else None

st.chat_message("assistant").write(resultado.text) if resultado else None
