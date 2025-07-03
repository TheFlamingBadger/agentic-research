from fastapi import FastAPI
from shared.llm_integrations.gemini_client import GetGemini
from shared.llm_integrations.models import ChatResponse, ChatRequests

# Init app
app = FastAPI()
llm = GetGemini()

# API Endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequests): # Runs this function on request
    response_text = llm.chat(request.prompt)
    
    return ChatResponse(response=response_text)
