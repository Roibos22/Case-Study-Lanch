from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from . import models, schemas
from typing import List, Optional, Tuple

class RankingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_ranking(self, ranking_data: dict) -> models.Ranking:
        """Create a new ranking entry"""
        db_ranking = models.Ranking(**ranking_data)
        self.db.add(db_ranking)
        self.db.commit()
        self.db.refresh(db_ranking)
        return db_ranking

    def bulk_create_rankings(self, rankings_data: List[dict]) -> None:
        """Bulk create ranking entries"""
        self.db.bulk_insert_mappings(models.Ranking, rankings_data)
        self.db.commit()

    def get_latest_ranking(self, slug: str) -> Optional[models.Ranking]:
        """Get the latest ranking for a restaurant"""
        return self.db.query(models.Ranking)\
            .filter(models.Ranking.slug == slug)\
            .order_by(models.Ranking.retrieved_at.desc())\
            .first()

    def get_rankings_history(
        self, 
        slug: str, 
        days: int = 7,
        limit: Optional[int] = None
    ) -> List[models.Ranking]:
        """Get ranking history for a restaurant"""
        query = self.db.query(models.Ranking)\
            .filter(
                models.Ranking.slug == slug,
                models.Ranking.retrieved_at >= datetime.now() - timedelta(days=days)
            )\
            .order_by(models.Ranking.retrieved_at.desc())
        
        if limit:
            query = query.limit(limit)
            
        return query.all()

    def get_rank_statistics(
        self, 
        slug: str, 
        days: int = 7
    ) -> Tuple[float, int, int]:
        """Get average, min, and max rank for a restaurant"""
        result = self.db.query(
            func.avg(models.Ranking.rank).label('avg_rank'),
            func.min(models.Ranking.rank).label('min_rank'),
            func.max(models.Ranking.rank).label('max_rank')
        ).filter(
            models.Ranking.slug == slug,
            models.Ranking.retrieved_at >= datetime.now() - timedelta(days=days)
        ).first()
        
        return result if result else (None, None, None)