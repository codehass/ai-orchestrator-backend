from fastapi import Depends
from sqlalchemy.orm import Session
from ...authentication.auth import get_current_user
from ...schemas.user_schema import UserSchema, AnalyzeRequest
from ...models.history_model import HistoryLogs
from ...db.database import get_db
from ...services.service_gemini import analyzer
import json
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/analyze",
)


@router.post("/")
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


@router.get("/")
def get_user_history(
    current_user: UserSchema = Depends(get_current_user), db: Session = Depends(get_db)
):
    logs = db.query(HistoryLogs).filter(HistoryLogs.user_id == current_user.id).all()

    return logs
