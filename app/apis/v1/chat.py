# app/routers/chat.py

from fastapi import APIRouter, HTTPException
from app.schemas.message import ChatRequest, ChatResponse, ChatMessage
from app.services.llm import LLMService
from app.services.stories import StoryService
from app.services.simulation import SimulationService 

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
                # If user wants a simulation → interactive scenario mode
        if request.generate_story:
            sim = SimulationService()
            # use the scenario the user sent, or default if they forgot
            scenario_title = request.scenario or  request.message 
            out = sim.step(
                history=request.history,
                user_input=request.message,
                scenario=scenario_title
            )
            return ChatResponse(
                reply=out["reply"],
                social_story=None,
                history=out["history"]
            )

        # System prompt (in Arabic, supportive tone, with emojis)
        system_msg = ChatMessage(
            role="assistant",
            content=(
               
                "تحدث بالعربية "
    
            )
        )

        # Build the messages list
        messages = (
            [ {"role": system_msg.role, "content": system_msg.content} ] +
            [ m.dict() for m in request.history ] +
            [ {"role": "user", "content": request.message} ]
        )

        # Call the LLM
        llm = LLMService()
        reply_text = llm.generate_response_with_history(messages)

        # Optional social story
        social_story = None
        if request.generate_story:
            social_story = StoryService().generate_social_story(request.message)

        # Build updated history
        new_history = request.history + [
            ChatMessage(role="user",      content=request.message),
            ChatMessage(role="assistant", content=reply_text)
        ]

        return ChatResponse(
            reply=reply_text,           # <-- use reply_text, not s.reply_text
            social_story=social_story,
            history=new_history
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
