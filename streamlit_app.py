import streamlit as st
from google import genai
from google.genai import types

# 1. Configuración de la interfaz de la aplicación
st.set_page_config(page_title="XISUS", page_icon="👩‍🦲", layout="centered")

# 2. Inicialización segura del cliente de la API de Gemini
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    cliente = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🔑 Error: No se encontró 'GEMINI_API_KEY' en st.secrets.")
    st.stop()

# 3. Diccionario con las directrices de personalidad
instrucciones = {
    "Normal": "Eres XISUS, tu calvito de confianza. Un asistente de IA útil.",
    "Amigable": "Eres XISUS, un asistente extremadamente amigable, entusiasta y cálido.",
    "Profesional": "Eres XISUS, un asistente serio, corporativo, formal y directo.",
    "Divertido": "Eres XISUS. Responde con mucho humor, bromas ligeras y buena onda.",
    "Conciso": "Eres XISUS. Da respuestas extremadamente cortas, al grano y sin rodeos."
}

# 4. Configuración en la Barra Lateral (Evita que estorbe en el chat)
st.sidebar.title("⚙️ Configuración de XISUS")

modelo_visual = st.sidebar.selectbox(
    "🧠 Modelo",
    ["gemini-2.5-flash", "gemini-2.5-pro"]
)

personalidad_visual = st.sidebar.selectbox(
    "🎨 Personalidad",
    ["Normal", "Amigable", "Profesional", "Divertido", "Conciso"]
)

# Botón para reiniciar la conversación por completo
if st.sidebar.button("🗑️ Borrar Historial"):
    if "chat_gemini" in st.session_state:
        del st.session_state["chat_gemini"]
    st.rerun()

# 5. Creación ÚNICA del chat con memoria en la sesión
# Al envolverlo en este 'if', Streamlit no lo destruirá al recargar la página
if "chat_gemini" not in st.session_state:
    configuracion_inicial = types.GenerateContentConfig(
        system_instruction=instrucciones[personalidad_visual],
        temperature=0.7
    )
    # Iniciamos la sesión de chat con memoria nativa de Google
    st.session_state.chat_gemini = cliente.chats.create(
        model=modelo_visual,
        config=configuracion_inicial
    )

# 6. Interfaz Principal del Chat
st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

# Dibujar el historial acumulado en la pantalla
historial_mensajes = st.session_state.chat_gemini.get_history()
for mensaje in historial_mensajes:
    # Mapeamos los roles de Google ('user'/'model') a los de Streamlit ('user'/'assistant')
    rol_streamlit = "user" if mensaje.role == "user" else "assistant"
    for parte in mensaje.parts:
        if parte.text:
            with st.chat_message(rol_streamlit):
                st.write(parte.text)

# 7. Cuadro de entrada de texto para el usuario
pregunta = st.chat_input("Escribe algo...")

if pregunta:
    # Mostrar inmediatamente el mensaje que acaba de escribir el usuario
    with st.chat_message("user"):
        st.write(pregunta)

    try:
        # Animación de carga mientras responde la API
        with st.spinner("XISUS está pensando..."):
            # Enviamos el mensaje al objeto chat que retiene toda la memoria de la sesión
            resultado = st.session_state.chat_gemini.send_message(pregunta)

        # Mostrar la respuesta en pantalla
        with st.chat_message("assistant"):
            st.write(resultado.text)
            
        # Forzar recarga rápida de Streamlit para sincronizar la UI correctamente
        st.rerun()

    except Exception as e:
        st.error("😕 XISUS ha tenido un problema al comunicarse con Gemini.")
        st.caption(f"Detalle técnico del error: {e}")

# Indicadores de estado inferiores en la barra lateral
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Estado de XISUS")
st.sidebar.success("🟢 Gemini conectado")
st.sidebar.info(f"🧠 Modelo: {modelo_visual}")
st.sidebar.info(f"🎨 Estilo: {personalidad_visual}")
)

