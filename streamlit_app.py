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

```
modelos = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite"
]

respuesta = None
modelo_usado = None

with st.chat_message("assistant"):
    with st.spinner("XISUS está pensando..."):
        for modelo in modelos:
            try:
                resultado = cliente.models.generate_content(
                    model=modelo,
                    contents=pregunta
                )

                if resultado.text:
                    respuesta = resultado.text
                    modelo_usado = modelo
                    break

            except Exception:
                continue

        if respuesta:
            st.write(respuesta)
            st.caption("🧠 Modelo utilizado: " + modelo_usado)
        else:
            st.error("😵‍💫 XISUS no ha podido responder.")
            st.warning(
                "Gemini está teniendo problemas temporalmente. "
                "Prueba de nuevo en unos segundos."
            )
```
