import requests
from urllib.parse import quote
import json
from datetime import datetime
import time
import logging
from typing import Dict, Optional
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import uuid

class LieferandoAPI:
    def __init__(self, 
                 delay_seconds: float = 1.0,
                 max_retries: int = 3):
        # Get the scraper directory path (assuming this file is in the scraper package)
        self.scraper_dir = Path(__file__).parent.resolve()
        
        # Setup output directory inside scraper folder
        self.output_dir = self.scraper_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        self.delay_seconds = delay_seconds
        self.session_id = str(uuid.uuid4())

        # Setup logging to scraper directory
        log_file = self.scraper_dir / 'lieferando_api.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        
        self.logger.info(f"Initialized LieferandoAPI. Output directory: {self.output_dir}")

        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def _rotate_session_id(self):
        self.session_id = str(uuid.uuid4())
        self.logger.info("Rotated to new session ID")

    def _get_headers(self) -> Dict[str, str]:
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'de',
            'cache-control': 'no-cache',
            'origin': 'https://www.lieferando.de',
            'pragma': 'no-cache',
            'referer': 'https://www.lieferando.de/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-country-code': 'de',
            'x-language-code': 'de',
            'x-requested-with': 'XMLHttpRequest',
            'x-session-id': self.session_id
        }

    def _make_request(self, url: str, params: Optional[Dict] = None, retry_count: int = 0) -> Dict:
        try:
            time.sleep(self.delay_seconds)
            response = self.session.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code in [401, 403] and retry_count < 3:
                self.logger.warning(f"Request failed with {response.status_code}, rotating session ID and retrying...")
                self._rotate_session_id()
                return self._make_request(url, params, retry_count + 1)
            self.logger.error(f"API request failed: {str(e)}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise

    def get_slug_address(self, slug: str) -> Dict:
        url = f'https://cw-api.takeaway.com/api/v34/restaurant?slug={quote(slug)}'
        restaurant_data = self._make_request(url)
        
        if not restaurant_data.get('location'):
            raise ValueError(f"No restaurant found for slug: {slug}")
            
        location = restaurant_data['location']

        return {
            #'deliveryAreaId': address_data['deliveryAreaId'],
            'postalCode': location['postalCode'],
            'lat': location['lat'],
            'lng': location['lng'],
            'limit': 0,
            'isAccurate': 'true',
            'filterShowTestRestaurants': 'false'
        }

    def get_restaurants_by_address(self, address: str) -> Dict:
        self.logger.info(f"Fetching restaurants for address: {address}")
    
        restaurants_url = 'https://cw-api.takeaway.com/api/v34/restaurants'
        result = self._make_request(restaurants_url, address)
        
        return result

    def save_response(self, data: Dict, address: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_address = "".join(x for x in address if x.isalnum() or x in (' ', '-', '_')).strip()
        filename = self.output_dir / f"restaurants_{safe_address}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Data saved to {filename}")
        return str(filename)