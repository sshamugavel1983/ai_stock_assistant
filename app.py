import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("AI Stock Market Research Assistant")

ticker = st.text_input("Enter stock ticker (e.g., AAPL, MSFT, TSLA)")

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Predict Stock Price") and ticker:
        response = requests.get(f"http://localhost:8000/predict?ticker={ticker}")
        if response.status_code == 200:
            data = response.json()
            if "predicted_price" in data:
                st.success(f"Predicted Price for {ticker}: **${data['predicted_price']:.2f}**")
            else:
                st.error(data["error"])
        else:
            st.error("Error fetching prediction.")

with col2:
    if ticker:
        st.subheader(f"Latest {ticker} News 📰")
        # Add news fetching function here
