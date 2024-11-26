from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from . import models, schemas
from typing import List, Optional, Tuple

class RankingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_ranking(self, ranking: dict) -> models.Ranking:
        db_ranking = models.Ranking(**ranking)
        self.db.add(db_ranking)
        self.db.commit()
        self.db.refresh(db_ranking)
        return db_ranking
