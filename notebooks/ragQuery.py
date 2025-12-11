from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load Environment Variables
# This reads from your .env file locally, or system variables in production/cloud
load_dotenv()

# Get API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    # Fail fast: If there is no key, stop the server immediately
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found. Please add it to your .env file.")

# Prepare Embeddings
# Downloads model if not cached
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the Vector Database
# Check if folder exists to avoid vague errors
if not os.path.exists("vector_db"):
    raise FileNotFoundError("The 'vector_db' folder was not found. Please run your ingestion script first.")

database = FAISS.load_local("vector_db", embeddings) 

# Create Retriever
# Increased k to 8 to improve recall (filtering out bibliographies)
retriever = database.as_retriever(search_kwargs={"k": 8})

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
    """
    This function is called by app.py (FastAPI).
    It returns the raw tuple: (Answer String, List of Source Documents)
    """
    ans = qna_chain({"query": q}) 
    return ans["result"], ans["source_documents"]