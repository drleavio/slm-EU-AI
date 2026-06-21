from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from groq import Groq
from ollama import Client

load_dotenv()
ollama_client = Client(host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))

app = FastAPI(title="SLM Backend API")

class GenerateRequest(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]

class ComplianceRequest(BaseModel):
    user_input: str

@app.get("/")
async def root():
    return {"message": "Welcome to the SLM Backend API"}

@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generate text based on a simple prompt.
    """
    try:
        response = ollama_client.generate(model='my-trained-slm', prompt=request.prompt)
        return {"response": response['response']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint accepting a list of messages.
    Example: {"messages": [{"role": "user", "content": "Hello"}]}
    """
    try:
        response = ollama_client.chat(model='my-trained-slm', messages=request.messages)
        return {"response": response['message']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/eu-ai-compliance")
async def eu_ai_compliance(request: ComplianceRequest):
    """
    Two-step compliance check:
    1. Extract details using Groq (fast LLM).
    2. Analyze compliance tier using the local SLM.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured in .env file")
    
    groq_client = Groq(api_key=api_key)
    
    # Step 1: Extract information using Groq
    extraction_prompt = f"""
You are an expert in the EU AI Act. The user will provide details about their AI system.
Extract the key information relevant to EU AI Act compliance, such as the intended purpose, 
the domain (e.g., employment, biometric, education), and any potential risk factors.

User Input: {request.user_input}

Extracted Information:
"""
    try:
        groq_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": extraction_prompt}],
            model="llama-3.1-8b-instant", # using a fast default groq model
            temperature=0.2,
        )
        extracted_info = groq_response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during Groq extraction: {str(e)}")

    # Step 2: Pass extracted information to the local SLM
    slm_prompt = f"""
Analyze the following extracted AI system details and determine its EU AI Act risk tier and rationale.

Details:
{extracted_info}
"""
    try:
        slm_response = ollama_client.generate(model='my-trained-slm', prompt=slm_prompt)
        final_analysis = slm_response['response']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from local SLM: {str(e)}")

    return {
        "extracted_information": extracted_info,
        "compliance_analysis": final_analysis
    }
