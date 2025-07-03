import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from ai.gemini import Gemini

# Init app
load_dotenv(find_dotenv())  # Load environment variables from .env file
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# AI agent config
def load_system_prompt():
    try:
        with open("src/prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)

# Pydantic Models
class ChatRequests(BaseModel):
    prompt:str
    
class ChatResponse(BaseModel):
    response:str
    
# API Endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequests): # Runs this function on request
    response_text = ai_platform.chat(request.prompt)
    
    return ChatResponse(response=response_text)
