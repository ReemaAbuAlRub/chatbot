from pydantic import BaseModel
from typing import List, Optional, Literal

class ChatMessage(BaseModel):
    role: Literal["user","assistant"]
    content: str

class ChatRequest(BaseModel):
    message: str
    generate_story: bool = False
    scenario: Optional[str] = None    
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    reply: str
    social_story: Optional[str] = None
    history: List[ChatMessage]
