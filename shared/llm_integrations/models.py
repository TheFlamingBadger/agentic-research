from pydantic import BaseModel

# Pydantic Models
class ChatRequests(BaseModel):
    prompt:str
    
class ChatResponse(BaseModel):
    response:str