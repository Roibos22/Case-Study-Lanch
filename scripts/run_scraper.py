import logging
from app.scraper.lieferando_scraper import LieferandoScraper
from typing import List
import time
from apscheduler.schedulers.blocking import BlockingScheduler

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
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scraper, 'cron', minute='*/1')
    scheduler.start()

if __name__ == "__main__":
    main()