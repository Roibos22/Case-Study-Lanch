import logging
from main import process_address
from typing import List, Dict
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ADDRESSES: List[Dict[str, str]] = [
    {
        "address": "50226 frechen",
        "restaurant": "loco-chicken-i-frechen"
    },
    {
        "address": "33615 bielefeld",
        "restaurant": "loco-chicken-bielefeld"
    },
    {
        "address": "50677 köln",
        "restaurant": "happy-slice-suedstadt"
    },
    {
        "address": "22089 hamburg",
        "restaurant": "happy-slice-pizza-i-wandsbek-markt"
    }
]

def run_scraper():
    """Process all hardcoded addresses"""
    logger.info("Beginning to process addresses")
    
    results = []
    for entry in ADDRESSES:
        address = entry["address"]
        restaurant = entry["restaurant"]
        
        try:
            logger.info(f"Processing {restaurant} at {address}")
            result = process_address(address, restaurant)
            results.append({
                "address": address,
                "restaurant": restaurant,
                "rank": result["rank"],
                "rank_total": result["rank_total"],
                "total_restaurants": result["total_restaurants"]
            })
            logger.info(f"Successfully processed {restaurant}")
            
            # Add delay between requests
            if entry != ADDRESSES[-1]:
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"Error processing {restaurant} at {address}: {e}")
            continue
    
    logger.info("\nScraping Summary:")
    for result in results:
        logger.info(
            f"Restaurant: {result['restaurant']:40} "
            f"Address: {result['address']:20} "
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