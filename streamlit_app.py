import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

API_KEY = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=API_KEY)

st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

pregunta = st.chat_input("Escribe algo...")

if pregunta:
    st.chat_message("user").write(pregunta)

    try:
        resultado = cliente.models.generate_content(
            model="gemini-3.5-flash",
            contents=pregunta
        )

        st.chat_message("assistant").write(resultado.text)

    except Exception as e:
        st.error("😕 XISUS ha tenido un problema al comunicarse con Gemini.")
        st.caption("Puedes intentar enviar la pregunta de nuevo.")


st.markdown("---")
st.subheader("⚙️ Configuración de XISUS")

modelo_visual = st.selectbox(
    "🧠 Modelo",
    [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash"
    ]
)

personalidad_visual = st.selectbox(
    "🎨 Personalidad",
    [
        "Normal",
        "Amigable",
        "Profesional",
        "Divertido",
        "Conciso"
    ]
)

st.markdown("---")
st.subheader("💬 Estado de XISUS")

st.success("🟢 Gemini conectado")

st.info("🧠 Modelo activo: " + modelo_visual)

st.info("🎨 Personalidad: " + personalidad_visual)
