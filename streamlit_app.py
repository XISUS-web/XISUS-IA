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

st.markdown("---")

st.subheader("⚙️ Configuración de XISUS")

col1, col2 = st.columns(2)

with col1:
st.markdown("### 🧠 Modelo")
st.selectbox(
"Modelo utilizado",
[
"gemini-3.5-flash",
"gemini-3.5-flash-lite",
"gemini-3.6-flash",
"gemini-3.7-flash"
],
index=0,
key="selector_modelo"
)

with col2:
st.markdown("### 🎨 Personalidad")
st.selectbox(
"Estilo de respuesta",
[
"Normal",
"Amigable",
"Profesional",
"Divertido",
"Conciso"
],
index=0,
key="personalidad"
)

st.markdown("---")

st.subheader("💬 Estado de XISUS")

st.success("🟢 Gemini conectado")

st.info(
"🧠 Modelo activo: " + st.session_state.get("selector_modelo", "gemini-3.5-flash")
)

st.info(
"🎨 Personalidad: " + st.session_state.get("personalidad", "Normal")
)



st.markdown("---")
st.subheader("⚙️ Configuración de XISUS")

modelo_visual = st.selectbox("🧠 Modelo", ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3.7-flash"])

personalidad_visual = st.selectbox("🎨 Personalidad", ["Normal", "Amigable", "Profesional", "Divertido", "Conciso"])

st.markdown("---")
st.subheader("💬 Estado de XISUS")

st.success("🟢 Gemini conectado")

st.info("🧠 Modelo activo: " + modelo_visual)

st.info("🎨 Personalidad: " + personalidad_visual)
