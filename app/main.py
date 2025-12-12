import os
from fastapi import FastAPI
from .db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import auth, analyze
from .config import settings

app = FastAPI(
    title="Articles Summary API",
    description=(
        "This API provides automatic text analysis using AI models. "
        "It performs zero-shot classification with HuggingFace, generates structured summaries using Gemini, "
        "detects sentiment, and stores results in a user-specific history. "
        "Includes authentication, filtering, and retrieval of past analyses."
    ),
)


origins = [settings.FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(analyze.router)


@app.get("/", tags=["Home route"])
def get_home():
    return {"message": "Hello API"}
