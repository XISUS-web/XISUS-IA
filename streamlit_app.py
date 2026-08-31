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
try:
    resultado = cliente.models.generate_content(
        model="gemini-3.5-flash",
        contents=pregunta
    )

    respuesta = resultado.text

    st.chat_message("assistant").write(respuesta)

except Exception as error:
    st.chat_message("assistant").error(
        "😵‍💫 XISUS no ha podido responder en este momento."
    )
    st.info(
        "Gemini está teniendo problemas temporalmente. "
        "Prueba de nuevo dentro de unos segundos."
    )
```
