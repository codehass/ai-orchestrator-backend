from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from ..db.database import Base


class HistoryLogs(Base):
    __tablename__ = "history_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False)
    category = Column(String, index=True)
    summary = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    sentiment = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="history_logs")
