import streamlit as st
from google import genai

st.set_page_config(
page_title="XISUS",
page_icon="👩‍🦲",
layout="centered"
)

API_KEY = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=API_KEY)

if "historial" not in st.session_state:
st.session_state.historial = []

if "modelo" not in st.session_state:
st.session_state.modelo = "gemini-3.5-flash"

st.sidebar.title("⚙️ Configuración de XISUS")

modelo = st.sidebar.selectbox(
"🧠 Modelo de Gemini",
[
"gemini-3.5-flash",
"gemini-3.5-flash-lite",
"gemini-3.6-flash",
"gemini-3.7-flash",
"gemini-3.1-flash-lite"
]
)

st.session_state.modelo = modelo

st.sidebar.markdown("---")

st.sidebar.subheader("💬 Conversación")

if st.sidebar.button("🆕 Nueva conversación", use_container_width=True):
st.session_state.historial = []
st.rerun()

if st.sidebar.button("🗑️ Borrar historial", use_container_width=True):
st.session_state.historial = []
st.rerun()

st.sidebar.markdown("---")

st.sidebar.subheader("👩‍🦲 XISUS")

st.sidebar.info(
"Tu calvito de confianza 🤖\n\n"
"Selecciona el modelo que quieras utilizar "
"desde el menú de arriba."
)

st.markdown(
"<h1 style='text-align:center;color:#FF4B4B;'>"
"👩‍🦲 XISUS"
"</h1>",
unsafe_allow_html=True
)

st.markdown(
"<p style='text-align:center;font-size:18px;'>"
"Tu calvito de confianza 🤖"
"</p>",
unsafe_allow_html=True
)

st.markdown("---")

for mensaje in st.session_state.historial:
st.chat_message(mensaje["rol"]).write(mensaje["texto"])

pregunta = st.chat_input(
"¿De qué quieres hablar hoy? 😎"
)

resultado = cliente.models.generate_content(
model=st.session_state.modelo,
contents=pregunta
) if pregunta else None

st.chat_message("user").write(pregunta) if pregunta else None

st.chat_message("assistant").write(
resultado.text
) if resultado else None

if pregunta:
st.session_state.historial.append(
{
"rol": "user",
"texto": pregunta
}
)


st.session_state.historial.append(
    {
        "rol": "assistant",
        "texto": resultado.text
    }
)

