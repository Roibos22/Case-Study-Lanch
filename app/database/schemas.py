from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class RankingCreate(BaseModel):
    slug: str
    rank: int
    true_rank: int
    sponsored: bool
    is_open: bool
    total_restaurants: int
    total_delivering: int
    total_open_delivering: int
    search_metadata: Optional[Dict] = None  # Changed from 'metadata' to 'search_metadata'

class Ranking(RankingCreate):
    id: int
    retrieved_at: datetime

    class Config:
        from_attributes = True