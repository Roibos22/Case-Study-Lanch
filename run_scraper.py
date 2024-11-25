import logging
from main import process_slug
from typing import List, Dict
import time

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
    logger.info("Beginning to process slugs")
    
    results = []
    for slug in SLUGS:
        try:
            logger.info(f"Processing {slug}")
            result = process_slug(slug)
            results.append({
                "slug": slug,
                "rank": result["rank"],
                "rank_total": result["rank_total"],
                "total_restaurants": result["total_restaurants"]
            })
            logger.info(f"Successfully processed {slug}")
            
            # Add delay between requests
            if entry != SLUGS[-1]:
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"Error processing {slug}: {e}")
            continue
    
    logger.info("\nScraping Summary:")
    for result in results:
        logger.info(
            f"Restaurant: {result['slug']:40} "
            f"Rank: {result['rank']:3} "
            f"Rank Total: {result['rank_total']:3} "
            f"Total Restaurants: {result['total_restaurants']}"
        )

if __name__ == "__main__":
    try:
        run_scraper()
    except KeyboardInterrupt:
        logger.info("Scraper stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)