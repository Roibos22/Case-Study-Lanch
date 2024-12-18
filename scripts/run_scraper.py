from app.scraper.lieferando_scraper import LieferandoScraper
from typing import List
from apscheduler.schedulers.blocking import BlockingScheduler
from app.utils.logger import setup_logger

logger = setup_logger("run_scraper")

SLUGS: List[str] = [
        "loco-chicken-i-frechen",
        "loco-chicken-bielefeld",
        "happy-slice-suedstadt",
        "happy-slice-pizza-i-wandsbek-markt"
]

def run_scraper():
    try:
        scraper = LieferandoScraper()
        scraper.process_slugs(SLUGS)
    except Exception as e:
        logger.error(f"Scraper Error: {e}")

def main():
    logger.info("Starting scheduler...")
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scraper, 'cron', minute='0', misfire_grace_time=3600)

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()

if __name__ == "__main__":
    main()