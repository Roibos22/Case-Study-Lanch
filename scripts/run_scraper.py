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

def main():
    try:
        scraper = LieferandoScraper()
        results = scraper.process_slugs(SLUGS)
        logger.info(f"Processed {len(results)} restaurants successfully")
    except Exception as e:
        logger.error(f"Scraper Error: {e}")

if __name__ == "__main__":
    main()