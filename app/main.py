
from fastapi import FastAPI
from app.api import chat
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  # Load API key, dsb.

app = FastAPI(
    title="Chatbot Sejarah dengan RAG + Gemini",
    version="1.0.0", # Version dari app 
    description= "Chatbot ini menggunakan API gemini 2.5 flash card dan rag untuk menghasilkan jawaban pertanyaan sejarah. " # Deskripsi
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan ["http://localhost:5173"] untuk lebih aman di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat")
