import streamlit as st
import ollama
from langdetect import detect, LangDetectException

st.title("💬 SII GROUP CHILE\n LLaMA 3 AI Generator")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "IT Engineer / Scrum Master", "content": "Escribe tu historia de usuario"}]

# Function to check if the input is in Spanish
def is_spanish(text):
    try:
        return detect(text) == 'es'
    except LangDetectException:
        return False

# Mostrar historial de chats
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

# Crear el generador de respuestas        
def generate_response():
    response = ollama.chat(model='llama3', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

# Agregar input de usuario y generador de respuestas
if prompt := st.chat_input():
    if is_spanish(prompt):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="🧑‍💻").write(prompt)
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
    else:
        st.error("Por favor, escribe tu historia de usuario en español.")
