# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import json
import time

class LieferandoScraper:
    def __init__(self):
        # Setup output directories
        self.output_dir = "data/raw_html"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("data/json", exist_ok=True)
        
        # Setup Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

    def save_page(self, url):
        """Save HTML and extracted JSON data for given URL"""
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            # Load page and wait for dynamic content
            driver.get(url)
            time.sleep(5)  # Basic wait for content to load
            
            # Generate timestamp for files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save complete HTML after JavaScript execution
            html_filename = f"{self.output_dir}/lieferando_{timestamp}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"HTML saved to: {html_filename}")
            
            # Extract JSON data
            scripts = driver.execute_script("return document.getElementsByTagName('script')")
            json_data = None
            for script in scripts:
                script_text = driver.execute_script("return arguments[0].textContent", script)
                if script_text and 'window.__INITIAL_STATE__' in script_text:
                    json_str = script_text.split('window.__INITIAL_STATE__ = ')[1].split('};')[0] + '}'
                    json_data = json.loads(json_str)
                    break
            
            if json_data:
                json_filename = f"data/json/lieferando_{timestamp}.json"
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2)
                print(f"JSON data saved to: {json_filename}")
            
            return html_filename, json_data

        except Exception as e:
            print(f"Error saving page: {e}")
            return None, None
            
        finally:
            driver.quit()

# Run scraper
if __name__ == "__main__":
    scraper = LieferandoScraper()
    test_url = "https://www.lieferando.de/lieferservice/essen/frechen-50226"
    html_file, json_data = scraper.save_page(test_url)