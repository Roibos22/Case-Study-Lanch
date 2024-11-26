import logging
from app.scraper.lieferando_scraper import LieferandoScraper
from typing import List
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
    try:
        scraper = LieferandoScraper()
        results = scraper.process_slugs(SLUGS)
        logger.info(f"Processed {len(results)} restaurants successfully")
    except Exception as e:
        logger.error(f"Scraper Error: {e}")

def main():
    while True:
        logger.info("Start new scraping routine")
        run_scraper()
        logger.info("End Scraping Routine")
        time.sleep(600)

if __name__ == "__main__":
    main()