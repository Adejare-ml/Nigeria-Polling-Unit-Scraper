import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from .config import NIGERIAN_STATES, MAX_PAGES, WARDS_URL, UNITS_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class INECScraper:
    def __init__(self, headless=True):
        self.driver = self._init_driver(headless)

    def _init_driver(self, headless):
        try:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome driver initialized successfully.")
            return driver
        except Exception as e:
            logger.error(f"Driver initialization failed: {e}")
            return None

    def _paginate_and_extract(self, url, target_state, columns_count):
        data = []
        seen = set()
        
        try:
            self.driver.get(url)
            time.sleep(3)
            page_num = 1

            while page_num <= MAX_PAGES:
                logger.info(f"Processing page {page_num} for {target_state}...")
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "table"))
                    )
                    rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
                    
                    if not rows:
                        break

                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= columns_count:
                            row_state = cells[0].text.strip()
                            if row_state.lower() == target_state.lower():
                                entry = tuple(cell.text.strip() for cell in cells[:columns_count])
                                if entry not in seen:
                                    data.append(entry)
                                    seen.add(entry)

                    next_button = self.driver.find_element(By.LINK_TEXT, "Next")
                    if next_button and next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)
                        page_num += 1
                    else:
                        break
                except (TimeoutException, NoSuchElementException):
                    break
        except Exception as e:
            logger.error(f"Error scraping {url} for {target_state}: {e}")
        
        return data

    def scrape_wards(self, state):
        return self._paginate_and_extract(WARDS_URL, state, 3)

    def scrape_units(self, state):
        return self._paginate_and_extract(UNITS_URL, state, 4)

    def close(self):
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed.")

def run_full_extraction():
    scraper = INECScraper()
    if not scraper.driver:
        return

    all_wards = []
    all_pus = []

    try:
        for state in NIGERIAN_STATES:
            logger.info(f"Processing State: {state}")
            wards = scraper.scrape_wards(state)
            all_wards.extend(wards)
            
            if wards:
                pus = scraper.scrape_units(state)
                all_pus.extend(pus)
            
            time.sleep(1)
        
        return all_wards, all_pus
    finally:
        scraper.close()
