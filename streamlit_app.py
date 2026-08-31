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

resultado = None
if pregunta:
    try:
        resultado = cliente.models.generate_content(model="gemini-2.5-flash", contents=pregunta)
    except Exception as e:
        st.write("ERROR:", type(e).__name__, getattr(e, "status_code", "SIN CÓDIGO"), str(e))

st.write(resultado.text if resultado else "Escribe una pregunta.")
