import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲", layout="centered")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.markdown(
"<h1 style='text-align:center;color:#FF4B4B;'>👩‍🦲 XISUS</h1>",
unsafe_allow_html=True
)

st.markdown(
"<p style='text-align:center;color:#888;'>Tu calvito de confianza 🤖</p>",
unsafe_allow_html=True
)

st.markdown("---")

modelos = [
"gemini-3.7-flash",
"gemini-3.6-flash",
"gemini-3.5-flash",
"gemini-3.5-flash-lite",
"gemini-3.1-flash-lite"
]

modelo = st.sidebar.selectbox(
"🧠 Modelo Gemini",
modelos,
index=1
)

st.sidebar.markdown("---")

temperatura = st.sidebar.slider(
"🌡️ Creatividad",
0.0,
2.0,
0.7,
0.1
)

max_tokens = st.sidebar.slider(
"📏 Longitud máxima",
256,
8192,
2048,
256
)

st.sidebar.markdown("---")
st.sidebar.info("Creado con orgullo por **Ernesto** 🚀")

pregunta = st.chat_input(
"¿De qué quieres hablar hoy? 😎"
)

def obtener_respuesta(texto):
try:
configuracion = types.GenerateContentConfig(
temperature=temperatura,
max_output_tokens=max_tokens
)

```
    respuesta = cliente.models.generate_content(
        model=modelo,
        contents=texto,
        config=configuracion
    )

    return respuesta.text

except Exception as e:
    codigo = getattr(e, "status_code", None)

    if codigo == 404:
        return "🔎 Ese modelo no está disponible para tu cuenta. Prueba otro modelo desde la barra lateral."

    if codigo == 403:
        return "🔐 Gemini ha rechazado el acceso. Comprueba tu API key y los permisos del proyecto."

    if codigo == 429:
        return "⏳ Has alcanzado temporalmente el límite de uso de Gemini. Espera un poco y vuelve a intentarlo."

    if codigo in [500, 502, 503, 504]:
        return "☁️ Gemini está teniendo problemas temporales. Espera unos segundos y vuelve a intentarlo."

    return "😕 XISUS ha tenido un problema al comunicarse con Gemini. Prueba de nuevo."
```

respuesta = obtener_respuesta(pregunta) if pregunta else None

st.write(respuesta if respuesta else "Escribe una pregunta para comenzar.")
