from fastapi import FastAPI, HTTPException
from app.scraper.lieferando_scraper import LieferandoScraper
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Restaurant Ranking API")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

@app.get("/rank/{restaurant_slug}")
async def get_rank(restaurant_slug: str):
    """Get the current ranking for a restaurant by its slug."""
    try:
        scraper = LieferandoScraper()
        result = scraper.process_slug(restaurant_slug, False)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
            
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

