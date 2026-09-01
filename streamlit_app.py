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
for mensaje in st.session_state.historial_google:
    # Vinculamos el rol de Google 'model' al rol 'assistant' de Streamlit
    rol_visual = "user" if mensaje["role"] == "user" else "assistant"
    with st.chat_message(rol_visual):
        st.write(mensaje["parts"][0])

pregunta = st.chat_input("Escribe algo...")

if pregunta:
    # 1. Mostrar tu pregunta en la pantalla de inmediato
    st.chat_message("user").write(pregunta)
    
    # 2. Guardar la pregunta en nuestro historial con la estructura oficial de Google
    st.session_state.historial_google.append({"role": "user", "parts": [pregunta]})

    try:
        # 3. Llamada directa y segura usando generate_content pasándole todo el historial acumulado
        resultado = cliente.models.generate_content(
            model="gemini-3.5-flash",
            contents=st.session_state.historial_google
        )

        # 4. Mostrar la respuesta en pantalla
        st.chat_message("assistant").write(resultado.text)
        
        # 5. Guardar la respuesta de la IA en el historial para el próximo turno
        st.session_state.historial_google.append({"role": "model", "parts": [resultado.text]})
        
        # Refrescar para ordenar la interfaz gráfica
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
