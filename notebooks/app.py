from fastapi import FastAPI
from pydantic import BaseModel
import os

# import functions that will be used directly
from notebooks.ragQuery import ask_question
from notebooks.riskScreening import calculate_risk

app = FastAPI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Models for incoming requests
class ChatQuery(BaseModel):
    question: str

class RiskInput(BaseModel):
    age: int
    bmi: float
    family_history: str
    symptoms_count: int

@app.get("/")
def home():
    return {"message": "Diabetes RAG API is running"}

# RAG Chatbot Endpoint
@app.post("/chat")
def chat(data: ChatQuery):
    answer, sources = ask_question(data.question)
    return {
        "answer": answer,
        "sources": [src.metadata for src in sources]
    }

# Diabetes Risk Screening Endpoint 
@app.post("/screen")
def screen(data: RiskInput):
    result = calculate_risk(
        age=data.age,
        bmi=data.bmi,
        family_history=data.family_history,
        symptoms_count=data.symptoms_count
    )
    return {"risk": result}
