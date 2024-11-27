import requests
from urllib.parse import quote
import time
from typing import Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import uuid
from app.utils.logger import setup_logger

class LieferandoAPIError(Exception):
    pass

class LieferandoAPI:
    def __init__(self, max_retries: int = 3):
        self.logger = setup_logger("app.api")
        self.session = self._create_session(max_retries)

    def _rotate_session_id(self):
        self.session_id = str(uuid.uuid4())
        self.logger.info("Rotated to new session ID")

    def _create_session(self, max_retries):
        session = requests.Session()
        retry_strategy = Retry(total=max_retries, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        self._rotate_session_id()
        return session

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
            response = self.session.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"API request to '{url}' failed: {str(e)}")
            raise LieferandoAPIError(f"API request to '{url}' failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request to '{url}' failed: {str(e)}")
            raise LieferandoAPIError(f"API request to '{url}' failed: {str(e)}")

    def _validate_location_data(self, location: Dict) -> bool:
        required_fields = ['postalCode', 'lat', 'lng']
        return all(field in location for field in required_fields)
    
    def _validate_restaurant_data(self, location: Dict) -> bool:
        required_fields = ['restaurants', 'aggregates']
        return all(field in location for field in required_fields)

    def get_slug_address(self, slug: str) -> Dict:
        url = f'https://cw-api.takeaway.com/api/v34/restaurant?slug={quote(slug)}'
        try:
            location_data = self._make_request(url)
        except LieferandoAPIError as e:
            self.logger.error(f"Error retrieving address data for slug '{slug}': {str(e)}")
            raise LieferandoAPIError(f"Error retrieving address data for slug '{slug}': {str(e)}")
        
        if not self._validate_location_data(location_data['location']):
            raise LieferandoAPIError(f"No restaurant location data found for slug: {slug}")
        
        return {
            #'deliveryAreaId': address_data['deliveryAreaId'],
            'postalCode': location_data['location']['postalCode'],
            'lat': location_data['location']['lat'],
            'lng': location_data['location']['lng'],
            'limit': 0,
            'isAccurate': 'true',
            'filterShowTestRestaurants': 'false'
        }

    def get_restaurants_by_address(self, addressParams: Dict) -> Dict:
        self.logger.info(f"Fetching restaurants with address params: {addressParams}")
        try:
            restaurants_data = self._make_request("https://cw-api.takeaway.com/api/v34/restaurants", addressParams)
        except LieferandoAPIError as e:
            self.logger.error(f"Error retrieving restaurant data with address params '{address_params}': {str(e)}")
            raise LieferandoAPIError(f"Error retrieving restaurant data with address params '{address_params}': {str(e)}")

        if not self._validate_restaurant_data(restaurants_data):
            raise ValueError(f"No restaurant location data found for slug: {slug}")
        
        return restaurants_data