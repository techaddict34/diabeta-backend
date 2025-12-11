from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import your logic
# Ensure python can find this. If 'notebooks' is a folder, this is correct.
from notebooks.ragQuery import ask_question
from notebooks.riskScreening import calculate_risk

load_dotenv()

app = FastAPI()

# ENABLE CORS (Essential for Frontend Integration)
app.add_middleware(
    CORSMiddleware,
    # In production, replace ["*"] with your specific frontend domain (e.g., ["http://localhost:5500"])
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Data Models
class ChatQuery(BaseModel):
    question: str

class RiskInput(BaseModel):
    age: int
    bmi: float
    family_history: str
    symptoms_count: int

@app.get("/")
def home():
    return {"status": "online", "message": "Diabetes RAG API is running"}

# Refactored for Clean JSON
@app.post("/chat")
def chat(data: ChatQuery):
    try:
        # Call the function from ragQuery.py
        answer, raw_sources = ask_question(data.question)
        
        # Process sources to be "Frontend Friendly"
        clean_sources = []
        for src in raw_sources:
            # Extract just the filename, not the full folder path
            full_source = src.metadata.get("source", "Unknown")
            filename = os.path.basename(full_source)
            
            clean_sources.append({
                "title": filename,
                "page": src.metadata.get("page", "N/A"),
                # Get first 200 chars as a snippet
                "snippet": src.page_content[:200] + "..." 
            })

        return {
            "answer": answer,
            "citations": clean_sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/screen")
def screen(data: RiskInput):
    try:
        result = calculate_risk(
            age=data.age,
            bmi=data.bmi,
            family_history=data.family_history,
            symptoms_count=data.symptoms_count
        )
        return {"risk": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))