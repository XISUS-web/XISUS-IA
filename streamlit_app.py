import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

API_KEY = st.secrets["GEMINI_API_KEY"]

cliente = genai.Client(api_key=API_KEY)

# Inicializamos el historial en memoria como una lista limpia de Google si no existe
if "historial_google" not in st.session_state:
    st.session_state.historial_google = []

st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

# --- BLOQUE VISUAL: Mostrar los mensajes anteriores en la interfaz ---
# --- BLOQUE VISUAL CORREGIDO: Mostrar los mensajes anteriores en la interfaz ---
for mensaje in st.session_state.historial_google:
    # Ahora leemos el atributo .role usando un punto (sintaxis de objeto)
    rol_visual = "user" if mensaje.role == "user" else "assistant"
    
    with st.chat_message(rol_visual):
        # Recorremos las partes nativas del objeto Content de Google
        for parte in mensaje.parts:
            if parte.text:
                st.write(parte.text)

pregunta = st.chat_input("Escribe algo...")

if pregunta:
    # 1. Mostrar tu pregunta en la pantalla de inmediato
    st.chat_message("user").write(pregunta)
    
    # Importamos las estructuras de datos nativas que la SDK exige para validar bien
    from google.genai import types

    # 2. Convertimos tu texto en un objeto "Part" real de Google
    parte_nativa = types.Part.from_text(text=pregunta)
    
    # 3. Guardamos el mensaje estructurado como un objeto Content real
    mensaje_nativo = types.Content(role="user", parts=[parte_nativa])
    st.session_state.historial_google.append(mensaje_nativo)

    try:
        # 4. Enviamos toda la lista de objetos Content acumulados. ¡Cero fallos de Pydantic!
        resultado = cliente.models.generate_content(
            model="gemini-3.5-flash",
            contents=st.session_state.historial_google
        )

        # 5. Mostrar la respuesta en pantalla
        st.chat_message("assistant").write(resultado.text)
        
        # 6. Convertimos la respuesta de XISUS en objeto Content y lo guardamos
        parte_respuesta = types.Part.from_text(text=resultado.text)
        respuesta_nativa = types.Content(role="model", parts=[parte_respuesta])
        st.session_state.historial_google.append(respuesta_nativa)
        
        # Refrescar la interfaz visual
        st.rerun()

    except Exception as e:
        st.error("😕 XISUS ha tenido un problema al comunicarse con Gemini.")
        st.caption(f"Detalle: {e}")

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
