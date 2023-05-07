import streamlit as st
import openai
import pdfplumber
import requests

# Set up OpenAI API key
openai.api_key = "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"

# Set up Streamlit app
st.set_page_config(page_title="Resume Enhancer", page_icon=":guardsman:")

# Define function to extract text from PDF file
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        text = ""
        for page in pages:
            text += page.extract_text()
    return text

# Define function to get suggestions from OpenAI API
def get_suggestions(prompt):
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7,
    )

    message = response.choices[0].text.strip()
    return message

# Set up Streamlit app layout
st.title("Resume Enhancer")
st.markdown("Upload your resume below to get suggestions for improvement.")

file = st.file_uploader("Upload PDF", type=["pdf"])

if file:
    # Extract text from PDF file
    text = extract_text_from_pdf(file)

    # Split text into smaller chunks
    max_chunk_size = 2000
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    # Get suggestions for each chunk
    suggestions = []
    for i, chunk in enumerate(chunks):
        prompt = f"Please provide suggestions for improving the following resume (chunk {i+1}):\n\n{chunk}\n\nSuggestions:"
        chunk_suggestions = get_suggestions(prompt).split("\n")
        suggestions += chunk_suggestions

    # Display suggestions
    st.markdown("## Suggestions")
    for i, suggestion in enumerate(suggestions):
        st.markdown(f"{i+1}. {suggestion}")
