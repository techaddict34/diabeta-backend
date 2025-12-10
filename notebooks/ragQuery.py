from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

load_dotenv() # Loads environment variables from .env into process .env
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") # Prepare the emebedding model
database = FAISS.load_local("vector_db", embeddings) # Load the stored document embeddings into memory for retrieval during Q&A
# Convert the FAISS vector store into a retriever that performs similarity search,
# returning the 3 most relevant document chunks for each user query
retriever = database.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini")

qna_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True) # Define the QA chain for later

def ask_question(q):
    ans = qna_chain({"query": q}) # Store the result after done the QA
    return ans["result"], ans["source_documents"] # "result" and "source_documents" are default keys from LangChain dictionary

if __name__ == "__main__":
    answer, sources = ask_question("Apa gejala awal Diabetes yang kamu rasakan?")
    print(answer) # Show answer
    print("\nSumber:") # Show upcoming sources
    for src in sources:
        print(src.metadata)