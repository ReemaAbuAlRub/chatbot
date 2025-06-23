# app/services/simulation.py

from app.services.llm import LLMService
from app.schemas.message import ChatMessage
from typing import List, Dict

class SimulationService:
    def __init__(self):
        self.llm = LLMService()

    def step(
        self,
        history: List[ChatMessage],
        user_input: str,
        scenario: str 
    ) -> Dict:
        system_prompt = (
        " أنت مساعد    "
        "تحدث بالعربية "
        )

        messages = (
            [ {"role":"system",    "content": system_prompt} ] +
            [ m.dict() for m in history ] +
            [ {"role":"user",      "content": user_input} ]
        )

        # Ask the LLM for the next “step + question”
        bot_reply = self.llm.generate_response_with_history(messages)

        new_history = history + [
            ChatMessage(role="user",      content=user_input),
            ChatMessage(role="assistant", content=bot_reply)
        ]

        return {"reply": bot_reply, "history": new_history}
