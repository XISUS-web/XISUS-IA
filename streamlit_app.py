import streamlit as st
from google import genai

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

API_KEY = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=API_KEY)

# Crear la sesión de chat con memoria nativa si no existe todavía
if "chat_gemini" not in st.session_state:
    # Vinculamos por defecto tu modelo estrella
    st.session_state.chat_gemini = cliente.chats.create(model="gemini-3.5-flash")
st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

# Dibujar en pantalla el historial que tiene guardado Gemini
historial_activo = st.session_state.chat_gemini.get_history()
for mensaje in historial_activo:
    # Convertimos el rol de Google ('model') al de Streamlit ('assistant')
    rol_streamlit = "user" if mensaje.role == "user" else "assistant"
    for parte in mensaje.parts:
        if parte.text:
            st.chat_message(rol_streamlit).write(parte.text)
pregunta = st.chat_input("Escribe algo...")

if pregunta:
    # 1. Mostrar de inmediato la pregunta del usuario en pantalla
    st.chat_message("user").write(pregunta)

    try:
        # 2. Enviar el mensaje a la sesión de chat permanente
        resultado = st.session_state.chat_gemini.send_message(pregunta)

        # 3. Mostrar la respuesta de XISUS
        st.chat_message("assistant").write(resultado.text)
        
        # 4. Refrescar la página para ordenar la interfaz correctamente
        st.rerun()

     except Exception as e:
        # Esto te mostrará en pantalla el motivo exacto del fallo
        st.error("😕 XISUS ha tenido un problema al comunicarse con Gemini.")
        st.caption(f"Detalle técnico del error: {e}")

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
