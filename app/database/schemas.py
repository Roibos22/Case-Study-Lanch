from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RankingCreate(BaseModel):
    slug: str
    rank: int
    rank_total: int
    total_restaurants: int 
    total_restaurants_delivering: int
    total_restaurants_delivering_open: bool
    isSponsored: bool
    isOpenForOrder: bool

class Ranking(RankingCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True