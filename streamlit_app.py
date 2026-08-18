
import streamlit as st
from google import genai

# 1. Tu configuración de la página con tu emoji calvo
st.set_page_config(page_title="XISUS", page_icon="👩‍🦲", layout="centered")

# Tu llave API real
LLAVE_API = st.secrets["GEMINI_API_KEY"]

# Inicializamos el cliente de Google y el historial de chat en la web
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=LLAVE_API)
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-3.6-flash")

if "historial" not in st.session_state:
    st.session_state.historial = []

# 2. AGREGA ESTÉTICA: Barra lateral izquierda para Ernest
with st.sidebar:
    st.image("https://i.postimg.cc/ZR3kqszT/IMG-20260818-WA0020.jpg", width=90)
    st.title("⚙️ Configuración")
    st.markdown("---")
    st.subheader("Desarrollador:")
    st.info("Creado con orgullo por **Ernest** 🚀")
    
    # Botón estético para vaciar la pantalla si se llena de texto
    if st.button("🗑️ Limpiar Historial", use_container_width=True):
        st.session_state.historial = []
        st.session_state.chat = st.session_state.client.chats.create(model="gemini-3.6-flash")
        st.rerun()

# 3. Tus títulos principales combinados con un toque estético centrado
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>👩‍🦲 Chatea libremente con XISUS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>¡Bienvenido! Chatea con XISUS.</p>", unsafe_allow_html=True)
st.markdown("---")

# Mostrar los mensajes anteriores en la pantalla visual
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["texto"])

# 4. Tu cuadro de texto personalizado
if pregunta := st.chat_input("De que quieres hablar hoy, tienes a tu calvito a disposicion"):
    # Mostrar lo que tú escribiste
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.historial.append({"rol": "user", "texto": pregunta})

    # Enviar a Google con AGREGA ESTÉTICA: Animación de "pensando..."
    with st.chat_message("assistant"):
        with st.spinner("XISUS está pensando..."):
            respuesta = st.session_state.chat.send_message(pregunta)
            st.markdown(respuesta.text)
        st.session_state.historial.append({"rol": "assistant", "texto": respuesta.text})
