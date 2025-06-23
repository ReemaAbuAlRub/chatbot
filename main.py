from fastapi import FastAPI
from app.apis.v1.chat import router as chat_router

app = FastAPI(debug=True)

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "Chatbot POC is running"}