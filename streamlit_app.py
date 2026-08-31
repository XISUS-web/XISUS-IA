import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="XISUS", page_icon="👩‍🦲")

LLAVE_API = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=LLAVE_API)

st.title("👩‍🦲 XISUS")
st.caption("Tu calvito de confianza 🤖")

modelo = st.sidebar.selectbox(
"🧠 Modelo Gemini",
[
"gemini-3.6-flash",
"gemini-3.7-flash",
"gemini-3.5-flash",
"gemini-3.5-flash-lite",
"gemini-3.1-flash-lite"
]
)

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

pregunta = st.chat_input("¿De qué quieres hablar hoy? 😎")

def responder(texto):
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

except Exception as error:
    codigo = getattr(error, "status_code", None)

    if codigo == 404:
        return "🔎 El modelo seleccionado no está disponible para tu cuenta."

    if codigo == 403:
        return "🔐 Tu API key no tiene permiso para utilizar este modelo."

    if codigo == 429:
        return "⏳ Has alcanzado el límite de uso. Espera un poco y vuelve a intentarlo."

    if codigo in [500, 502, 503, 504]:
        return "☁️ Gemini está teniendo problemas temporales. Inténtalo de nuevo en unos segundos."

    return "😕 XISUS no ha podido comunicarse con Gemini."
```

respuesta = responder(pregunta) if pregunta else None

st.write(respuesta if respuesta else "👋 ¡Hola! Escribe algo para comenzar.")
