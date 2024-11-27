from fastapi import FastAPI, HTTPException
from app.scraper.lieferando_scraper import LieferandoScraper
import logging
from app.utils.logger import setup_logger

logger = setup_logger("app")

app = FastAPI(title="Lieferando Ranking API")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Connected to PostgreSQL database=lieferando_db host=db-1 port=5432")
    logger.info(f"Server listening on port=8080 host=0.0.0.0")

@app.get("/rank/{restaurant_slug}")
async def get_rank(restaurant_slug: str):
    logger.info(f"Processing ranking request for restaurant={restaurant_slug}")
    try:
        scraper = LieferandoScraper()
        result = scraper.process_slug(restaurant_slug, False)
        
        if "error" in result:
            logger.error(f"Restaurant not found: {restaurant_slug}")
            raise HTTPException(status_code=404, detail=result["error"])
        
        logger.info(
            f"Ranking retrieved restaurant={restaurant_slug} rank={result['rank']} "
            f"total={result['total_restaurants']} sponsored={result['isSponsored']}"
        )
        
        return {
            "restaurant_slug": restaurant_slug,
            "rank": result["rank"],
            "total_restaurants": result["total_restaurants"],
            "is_sponsored": result["isSponsored"],
            "is_open": result["isOpenForOrder"]
        }
        
    except Exception as e:
        logger.error(f"Error processing request for {restaurant_slug}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving ranking: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
