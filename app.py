import streamlit as st
import json
from llm_gap import generate_gap_analysis

st.title("AI Overview Content Gap Analyzer")

keyword = st.text_input("Enter Keyword")
client_url = st.text_input("Enter Client URL")

if st.button("Run Analysis"):
    st.write("Running analysis...")

    # Example input
    ai_sources = [{"url": "example.com"}]
    client_article = {"url": client_url}

    result = generate_gap_analysis(ai_sources, client_article)

    st.subheader("Gap Analysis Result")
    st.write(result)