import streamlit as st
import requests

st.title("AI Stock Market Research Assistant")
query = st.text_input("Enter your question:")

if query:
    api_url = f"https://ai-stock-assistant-backend-49980583353.us-central1.run.app/query?question={query}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        st.write(response.json()["response"])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching response: {e}")
