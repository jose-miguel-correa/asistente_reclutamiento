import ollama
import streamlit as st



def generate_answer(prompt):
    response = ollama.chat(model='llama3', messages=[{"role": "assistant", "content": prompt}])
    return response

context = """
            Curriculums:
            Nombre: jose miguel
            10 años de experiencia
            Dominio de python y sql
            Nombre: juanito perez
            3 años de experiencia
            Dominio de Java y PHP

            Clientes:
            Banco Estado
            Stack:
            Java
            PHP
            aceptando postulantes: no

            Banco Santander
            Stack:
            SQL
            Python
            aceptando postulantes: si

            Si el cliente no está aceptando postulantes no se puede asignar a nadie aunque tenga el dominio que forma parte del stack del cliente.
          """
# user_input = "puedo asignar a jose miguel en banco estado?"

#prompt = f"{context}\n\nUser Input: {user_input}\n\nLLaMA 3 Response:"
#answer = generate_answer(prompt)

logo_url = './logo.gif'
st.image(logo_url, width=100)

st.html("<h3>Asistente de Reclutamiento (llama3 based)</h3")

user_input = st.text_area("Escriba su pregunta:")

if st.button("Analizar"):
    if user_input:
        # Create prompt with context and user input
        prompt = f"{context}\n\nUser Input: {user_input}\n\nLLaMA 3 Response:"
        answer = generate_answer(prompt)  # Call the simplified function
        response_content = answer['message']['content']

        # Create a set of words from the context
        #context_words = set(context.lower().split())

        # Check if any word from the context is in the response
        #if any(word in response_content.lower() for word in context_words):
        st.write("Respuesta:")
        st.write(response_content)  # Display the full answer
        #else:
        #    st.warning("La respuesta no está relacionada con el contexto de reclutamiento.")
    else:
        st.warning("Sólo se aceptan preguntas relacionadas al reclutamiento.")



#print(answer['message']['content'])