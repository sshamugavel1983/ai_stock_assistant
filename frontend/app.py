import requests
import streamlit as st

st.title("AI Stock Market Research Assistant")
query = st.text_input("Enter your question:")

if query:
    api_url = f"http://127.0.0.1:8000/query?question={query}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise an error if status code is not 200
        st.write(response.json()["response"])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching response: {e}")
