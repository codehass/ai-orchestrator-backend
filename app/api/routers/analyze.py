from fastapi import Depends, Query
from sqlalchemy.orm import Session
from ...authentication.auth import get_current_user
from ...schemas.user_schema import UserSchema, AnalyzeRequest, AnalyzeResponse
from ...models.history_model import HistoryLogs
from ...db.database import get_db
from ...services.service_gemini import analyzer
import json
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/analyze", tags=["Analyze routes"])


@router.post("/")
def analyze_text(
    body: AnalyzeRequest,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    text = body.text
    is_public = body.is_public

    result = analyzer(text)

    if isinstance(result, str):
        result = json.loads(result)

    category = result["category"]
    score = result["score"]
    summary = result["summary"]
    sentiment = result["sentiment"]
    title = result["title"]

    new_article = HistoryLogs(
        user_id=current_user.id,
        category=category,
        summary=summary,
        score=score,
        sentiment=sentiment,
        title=title,
        is_public=is_public,
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


@router.get("/")
def get_user_history(
    current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)
):
    logs = db.query(HistoryLogs).filter(HistoryLogs.user_id == current_user.id).all()

    return logs


@router.get("/search", response_model=list[AnalyzeResponse])
def get_filtered_articles(
    category: str | None = None,
    sentiment: str | None = None,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(HistoryLogs).filter(HistoryLogs.user_id == current_user.id)

    if category:
        query = query.filter(HistoryLogs.category == category)

    if sentiment:
        query = query.filter(HistoryLogs.sentiment == sentiment)

    return query.offset(skip).limit(limit).all()


@router.get("/public", response_model=list[AnalyzeResponse])
def get_public_articles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
):

    logs = (
        db.query(HistoryLogs)
        .filter(HistoryLogs.is_public == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return logs
