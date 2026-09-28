from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rag import answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://longlife.bizfatt.com" , "www.longlife.bizfatt.com","http://localhost:5500"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=500)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(body: ChatIn):
    return {"reply": answer(body.message)}