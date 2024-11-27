from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RankingCreate(BaseModel):
    restaurant_slug: str
    rank: Optional[int]
    rank_overall: Optional[int]
    restaurants_delivery: Optional[int]
    restaurants_total: Optional[int]
    is_sponsored: bool = False
    is_active: bool = False 
    rating_votes: Optional[int]
    rating_score: Optional[float]

class Ranking(RankingCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True