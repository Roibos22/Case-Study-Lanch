from fastapi import FastAPI, HTTPException
from app.scraper.lieferando_scraper import LieferandoScraper, LieferandoAPIError
from app.utils.logger import setup_logger
from app.database.schemas import RankingCreate

logger = setup_logger("app")

app = FastAPI(title="Lieferando Ranking API")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Connected to PostgreSQL database=lieferando_db host=db-1 port=5432")
    logger.info(f"Server listening on port=8080 host=0.0.0.0")

@app.get("/rank/{restaurant_slug}", response_model=RankingCreate)
async def get_rank(restaurant_slug: str):
    """
    Retrieve the ranking information for a given restaurant.

    Args:
        restaurant_slug (str): The slug of the restaurant.

    Returns:
        dict: A dictionary containing the ranking information.
    """
    logger.info(f"Processing ranking request for restaurant={restaurant_slug}")
    try:
        scraper = LieferandoScraper()
        result = scraper.process_slug(restaurant_slug, False)
        if "error" in result:
            logger.error(f"Restaurant not found: {restaurant_slug}")
            raise HTTPException(status_code=404, detail=result["error"])
        logger.info(f"Ranking retrieved restaurant={restaurant_slug} rank={result['rank']} ")
        return RankingCreate(**result)
    except LieferandoAPIError as e:
        logger.error(f"Error processing '{restaurant_slug}': {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing request for {restaurant_slug}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving ranking for slug {restaurant_slug} - {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
