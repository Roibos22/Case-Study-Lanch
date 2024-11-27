
---
## Technical Architecture Design
---

**Components / Services**:
1. **LieferandoScraper and LieferandoAPI**
- gets called every 60 min by cron job
- LieferandoScraper receives list of slugs, goes through them one by one
- calls LieferandoAPI with slug name to get address of slug
- calls LiefarandoAPI with address to get data of restaurants at location
- stores data in Database

2. **Database Service** (PostgreSQL)
- Stores historical rankings
- has one table -> lieferando_rankings
- schema:
```
    id: int
    restaurant_slug: str
    rank: Optional[int]
    rank_overall: Optional[int]
    restaurants_delivery: Optional[int]
    restaurants_total: Optional[int]
    is_sponsored: bool = False
    is_active: bool = False 
    rating_votes: Optional[int]
    rating_score: Optional[float]
    timestamp: datetime
```

3. **API Service** (FastAPI)
- Handles GET /rank/<slug> requests
- Initiate LieferandoScraper
- Returns fresh rank data from Lieferando Scraper
- does not store in DB
