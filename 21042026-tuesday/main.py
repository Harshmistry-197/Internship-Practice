import streamlit as st
st.title("RAG Based Chatbot")
from app import ask_question

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("RAG-based Chatbot")
st.write("Ask me questions based on company policies, FAQs, and product manuals.")

# Chat input
query = st.text_input("Your question:")

if query:
    with st.spinner("Thinking..."):
        answer, sources = ask_question(query)

    st.markdown("###  Answer")
    st.write(answer)

    st.markdown("###  Sources")
    for src in sources:
        st.write(f"- {src}")
