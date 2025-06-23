import os
from openai import OpenAI
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_response_with_history(self, history: list[dict]) -> str:

        resp = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history,
            temperature=0.3,   
        )
        return resp.choices[0].message.content
