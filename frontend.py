# frontend.py - Simple Streamlit interface
import streamlit as st
import requests

st.title("🤖 AI Travel Assistant")

# Chat Section
st.header("Chat with AI")
message = st.text_input("Ask me anything:")
if message:
    response = requests.get(f"http://localhost:8000/api/chat?message={message}").json()
    st.write(f"**AI:** {response['response']}")

# Travel Planning
st.header("Plan a Trip")
destination = st.text_input("Destination", "Paris")
days = st.slider("Days", 1, 30, 3)
budget = st.number_input("Budget ($)", 100, 10000, 1000)

if st.button("Plan Trip"):
    response = requests.get(f"http://localhost:8000/api/travel/plan?destination={destination}&days={days}&budget={budget}").json()
    st.json(response)