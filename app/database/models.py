from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from . import Base

class Ranking(Base):
    __tablename__ = "restaurant_rankings"

    id = Column(Integer, primary_key=True)
    slug = Column(String, index=True, nullable=False)
    rank = Column(Integer, nullable=False)
    rank_total = Column(Integer, nullable=False)
    total_restaurants = Column(Integer, nullable=False)
    total_restaurants_delivering = Column(Integer, nullable=False)
    total_restaurants_delivering_open = Column(Integer, nullable=False)
    isSponsored = Column(Boolean, default=False)
    isOpenForOrder = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
