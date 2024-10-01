import streamlit as st
import requests
import PyPDF2
import io
import ollama

# Function to load the PDF and TXT files and extract text
def load_files(pdf_file, txt_file):
    # Extract text from PDF
    pdf_text = ""
    if pdf_file is not None:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"
    
    # Extract text from TXT
    txt_text = ""
    if txt_file is not None:
        txt_text = txt_file.read().decode("utf-8")  # Decode bytes to string
    
    return pdf_text, txt_text

# Generate LLaMA 3 answer using Ollama API
def generate_answer(prompt):
    response = ollama.chat(model='llama3', stream=True, messages=[{"role": "user", "content": prompt}])
    
    # Initialize an empty string to store the full response
    full_message = ""
    
    # Stream response and yield tokens
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        full_message += token
        yield token

# Streamlit app
st.title("LLaMA 3 Text Analyzer")

# File upload for PDF and TXT
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
txt_file = st.file_uploader("Upload a TXT file", type=["txt"])

# Load text from files if uploaded
if pdf_file or txt_file:
    pdf_text, txt_text = load_files(pdf_file, txt_file)
    context = pdf_text + "\n" + txt_text
    st.write("Context extracted from files:")
    st.write(context)

    # Input text for analysis
    user_input = st.text_area("Enter text to analyze:")

    if st.button("Analyze"):
        if user_input:
            # Create prompt with context and user input
            prompt = f"{context}\n\nUser Input: {user_input}\n\nLLaMA 3 Response:"
            response_tokens = generate_answer(prompt)
            
            # Display the response as it streams in
            st.write("LLaMA 3 Answer:")
            for token in response_tokens:
                st.write(token)  # Stream the response token by token
        else:
            st.warning("Please enter text to analyze.")
else:
    st.info("Please upload a PDF and/or TXT file for context.")
