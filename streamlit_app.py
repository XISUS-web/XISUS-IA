import streamlit as st
from google import genai
from google.genai import types

# 1. Configuración de la interfaz visual
st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

# 2. Inicialización del cliente de la API con tu clave secreta
API_KEY = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=API_KEY)

# 3. Inicialización del historial con la estructura nativa de Google
if "historial_google" not in st.session_state:
    st.session_state.historial_google = []

st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

# 4. BLOQUE VISUAL: Mostrar los mensajes de la sesión en la pantalla
for mensaje in st.session_state.historial_google:
    rol_visual = "user" if mensaje.role == "user" else "assistant"
    with st.chat_message(rol_visual):
        for parte in mensaje.parts:
            if parte.text:
                st.write(parte.text)

# 5. Entrada de texto del usuario
pregunta = st.chat_input("Escribe algo...")

# 6. Captura de la selección de configuración de los menús inferiores
st.markdown("---")
st.subheader("⚙️ Configuración de XISUS")

modelo_visual = st.selectbox(
    "🧠 Modelo",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro"
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

# Diccionario de instrucciones según la personalidad elegida
instrucciones = {
    "Normal": "Eres XISUS, tu calvito de confianza. Un asistente de IA útil.",
    "Amigable": "Eres XISUS, un asistente extremadamente amigable y cálido.",
    "Profesional": "Eres XISUS, un asistente serio, corporativo y formal.",
    "Divertido": "Eres XISUS. Responde con mucho humor y bromas ligeras.",
    "Conciso": "Eres XISUS. Da respuestas extremadamente cortas y al grano."
}

# Botón para vaciar la memoria del chat cuando quieras reiniciar la cuota
if st.button("🗑️ Limpiar historial de chat"):
    st.session_state.historial_google = []
    st.rerun()

# 7. LÓGICA DE EJECUCIÓN (Se activa al enviar una pregunta)
if pregunta:
    # Dibujar tu pregunta en pantalla de inmediato
    st.chat_message("user").write(pregunta)
    
    # Empaquetar la pregunta en un formato compatible con Pydantic y Google
    parte_nativa = types.Part.from_text(text=pregunta)
    mensaje_nativo = types.Content(role="user", parts=[parte_nativa])
    st.session_state.historial_google.append(mensaje_nativo)

    try:
        # Configurar la instrucción de sistema dinámica antes de llamar a la API
        configuracion = types.GenerateContentConfig(
            system_instruction=instrucciones[personalidad_visual]
        )

        # Enviar la conversación completa usando el modelo elegido en el selector
        resultado = cliente.models.generate_content(
            model=modelo_visual,
            contents=st.session_state.historial_google,
            config=configuracion
        )

        # Mostrar la respuesta de XISUS en pantalla
        st.chat_message("assistant").write(resultado.text)
        
        # Guardar la respuesta del modelo en la memoria
        parte_respuesta = types.Part.from_text(text=resultado.text)
        respuesta_nativa = types.Content(role="model", parts=[parte_respuesta])
        st.session_state.historial_google.append(respuesta_nativa)
        
        st.rerun()

    except Exception as e:
        st.error("😕 XISUS ha tenido un problema al comunicarse con Gemini.")
        st.caption(f"Detalle técnico del error: {e}")

st.markdown("---")
st.subheader("💬 Estado de XISUS")
st.success("🟢 Gemini conectado")
st.info("🧠 Modelo activo: " + modelo_visual)
st.info("🎨 Personalidad: " + personalidad_visual)
