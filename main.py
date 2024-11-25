# main.py
from app.scraper.lieferando_api import LieferandoAPI
from app.parser.restaurant_parser import RestaurantParser
import logging
from app.database import SessionLocal, engine, Base
from app.database.repository import RankingRepository
from app.database.schemas import RankingCreate

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

def store_ranking(ranking_data: dict):
    """Store ranking data in the database"""
    db = SessionLocal()
    try:
        repo = RankingRepository(db)
        ranking = repo.create_ranking(ranking_data)
        return ranking
    finally:
        db.close()

def process_slug(slug: str) -> dict:
    logger.info(f"Processing restaurant: {slug}")
    
    try:
        # Initialize API with delay
        api = LieferandoAPI(delay_seconds=2.0)
        
        # First get restaurant details and address from slug
        restaurant_data = api.get_restaurant_by_slug(slug)
        location = restaurant_data['location']
        address = f"{location['postalCode']} {location['city']}"
        
        # Get all restaurants data for that address
        result = api.get_restaurants_by_address(address)
        filename = api.save_response(result, address)
        logger.info(f"Data saved to: {filename}")
        
        # Parse restaurant data
        parser = RestaurantParser(result)
        parsed_ranking = parser.parse_restaurant(slug)
        logger.info(f"Parsed ranking data: {parsed_ranking}")
        
        # Store in database
        ranking = store_ranking(parsed_ranking)
        logger.info(f"Stored ranking with ID: {ranking.id}")
        
        return parsed_ranking
        
    except Exception as e:
        logger.error(f"Error processing {slug}: {str(e)}")
        raise


# if __name__ == "__main__":
#     # For testing purposes
#     test_address = "50226 frechen"
#     test_slug = "loco-chicken-i-frechen"
#     process_address(test_address, test_slug)