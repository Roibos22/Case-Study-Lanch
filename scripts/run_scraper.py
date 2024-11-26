import logging
from app.main import LieferandoScraper
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SLUGS: List[str] = [
        "loco-chicken-i-frechen",
        "loco-chicken-bielefeld",
        "happy-slice-suedstadt",
         "happy-slice-pizza-i-wandsbek-markt"
]

def run_scraper():
    try:
        scraper = LieferandoScraper()
        results = scraper.process_slugs(SLUGS)
        
        # Print summary
        logger.info("\nScraping Results:")
        for result in results:
            logger.info(
                f"Restaurant: {result['slug']:40} "
                f"Rank: {result['rank']}/{result['rank_total']} "
                f"Total Restaurants: {result['total_restaurants']}"
            )
            
    except KeyboardInterrupt:
        logger.info("Scraper stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    run_scraper()