from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
import streamlit as st  # Added to access Cloud Secrets
from dotenv import load_dotenv

load_dotenv() # Loads environment variables from .env (Local Mac)

# Prepare Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the Vector Database
database = FAISS.load_local("vector_db", embeddings) 

# Create Retriever
retriever = database.as_retriever(search_kwargs={"k": 3})

# Robustly find the API Key and check Local .env
groq_api_key = os.getenv("GROQ_API_KEY")

# Check Streamlit Secrets (Cloud)
if not groq_api_key:
    try:
        if "GROQ_API_KEY" in st.secrets:
            groq_api_key = st.secrets["GROQ_API_KEY"]
    except (FileNotFoundError, AttributeError):
        pass # Ignore errors if not running inside Streamlit

# Validation
if not groq_api_key:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found. Please set it in .env or Streamlit Secrets.")

# Initialize LLM with Groq
llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=groq_api_key,
    temperature=0
)

# Define the Chain
qna_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    retriever=retriever, 
    return_source_documents=True
)

def ask_question(q):
    ans = qna_chain({"query": q}) 
    return ans["result"], ans["source_documents"]

if __name__ == "__main__":
    # Test it locally
    answer, sources = ask_question("Apa gejala awal Diabetes yang kamu rasakan?")
    print(f"Answer: {answer}")
    print("\nSumber:")
    for src in sources:
        print(src.metadata)