import streamlit as st
# Import your actual RAG function
# Assuming you have a function 'ask_question(query)' in notebooks/ragQuery.py
from notebooks.ragQuery import ask_question 

st.set_page_config(page_title="Diabetes RAG Bot")
st.title("🤖 Diabetes Guidelines Assistant")

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. React to User Input
if prompt := st.chat_input("Ask about the guidelines..."):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Get Answer from your RAG
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Call your existing backend logic
                # Ensure ask_question returns a string
                response = ask_question(prompt) 
                
                # If your function returns a dictionary/chain result, extract the text:
                # response = response['result'] 
                
                st.markdown(response)
                
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")