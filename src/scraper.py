import logging
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from .config import NIGERIAN_STATES, MAX_PAGES, WARDS_URL, UNITS_URL, NEXT_PAGE_SELECTORS

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
            return driver
        except Exception as e:
            logger.error(f"Driver initialization failed: {e}")
            return None

    def _find_next_button(self):
        """Tries multiple selectors to find the 'Next' button."""
        for selector in NEXT_PAGE_SELECTORS:
            try:
                # If selector is a simple string like 'link', we might need to handle it specifically
                if selector == "link":
                    button = self.driver.find_element(By.LINK_TEXT, "Next")
                else:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if button.is_enabled():
                    return button
            except NoSuchElementException:
                continue
        return None

    def _paginate_and_extract(self, url, target_state, columns_count):
        data = []
        seen = set()
        
        try:
            self.driver.get(url)
            time.sleep(3)
            page_num = 1

            while page_num <= MAX_PAGES:
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

                    next_button = self._find_next_button()
                    if next_button:
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

    def scrape_state_data(self, state):
        """Orchestrates the extraction of both wards and units for a specific state."""
        logger.info(f"Worker initiating extraction for State: {state}")
        wards = self._paginate_and_extract(WARDS_URL, state, 3)
        pus = []
        if wards:
            pus = self._paginate_and_extract(UNITS_URL, state, 4)
        
        return state, wards, pus

    def close(self):
        if self.driver:
            self.driver.quit()

def run_full_extraction(max_workers=4):
    """
    Executes a parallelized extraction of electoral data.
    
    Args:
        max_workers: Number of concurrent browser instances.
    """
    all_wards = []
    all_pus = []
    
    # Use ThreadPoolExecutor to parallelize state extraction
    # Note: Each worker needs its own INECScraper (and thus its own driver)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a map of futures
        future_to_state = {executor.submit(worker_task, state): state for state in NIGERIAN_STATES}
        
        for future in as_completed(future_to_state):
            state = future_to_state[future]
            try:
                res_state, res_wards, res_pus = future.result()
                all_wards.extend(res_wards)
                all_pus.extend(res_pus)
                logger.info(f"Successfully completed extraction for {state}")
            except Exception as e:
                logger.error(f"State {state} failed during extraction: {e}")

    return all_wards, all_pus

def worker_task(state):
    """Task executed by the thread pool: Init driver -> Scrape -> Close driver."""
    scraper = INECScraper(headless=True)
    if not scraper.driver:
        return state, [], []
    try:
        return scraper.scrape_state_data(state)
    finally:
        scraper.close()
