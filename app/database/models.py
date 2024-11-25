from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from . import Base

class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True)
    slug = Column(String, index=True, nullable=False)
    rank = Column(Integer, nullable=False)
    true_rank = Column(Integer, nullable=False)
    sponsored = Column(Boolean, default=False)
    is_open = Column(Boolean, default=True)
    total_restaurants = Column(Integer)
    total_delivering = Column(Integer)
    total_open_delivering = Column(Integer)
    retrieved_at = Column(DateTime(timezone=True), server_default=func.now())
    search_metadata = Column(JSON)