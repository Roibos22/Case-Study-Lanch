from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from . import Base

class Ranking(Base):
    __tablename__ = "lieferando_rankings"

    id = Column(Integer, primary_key=True)
    slug = Column(String, index=True, nullable=False)
    rank = Column(Integer, nullable=True)
    rank_overall = Column(Integer, nullable=True)
    restaurants_delivery = Column(Integer, nullable=True)
    restaurants_total = Column(Integer, nullable=True)
    is_sponsored = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    rating_votes = Column(Integer, nullable=True)
    rating_score = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
