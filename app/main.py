import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .authentication.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from .schemas.user_schema import UserSchema, UserCreate, AnalyzeRequest
from .models.user_model import User
from .models.history_model import HistoryLogs
from .db.database import engine, Base, get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
from .services.service_gemini import analyzer
import json


load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()

origins = [FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.post("/auth/register", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/auth/login")
async def login_for_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INcorrect username or password",
            headers={"X-Authentication-Error": "Cookie not found or invalid"},
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=timedelta(hours=1),
    )
    return {"msg": "Login successful!"}


@app.post("/auth/logout")
async def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="Strict",
        path="/",
    )
    return {"msg": "Logged out successfully!"}


@app.get("/auth/me")
async def get_auth(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return {"authenticated": False}
    return {"authenticated": True}


@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@app.post("/analyze")
def analyze_text(
    body: AnalyzeRequest,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    text = body.text
    result = analyzer(text)

    if isinstance(result, str):
        result = json.loads(result)

    category = result["category"]
    score = result["score"]
    summary = result["summary"]
    sentiment = result["sentiment"]

    new_article = HistoryLogs(
        user_id=current_user.id,
        category=category,
        summary=summary,
        score=score,
        ton=sentiment,
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


@app.get("/")
def get_home():
    return {"message": "Hello API"}
