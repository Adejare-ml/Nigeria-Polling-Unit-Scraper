import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

# Simple wrapper for the legacy scraper function to maintain some compatibility
# in the new structure if needed.
def legacy_scrape(url, focus_level, state_filter):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table")
        if not table: return None
        
        headers = [th.text.strip() for th in table.find_all("th")]
        rows = [[td.text.strip() for td in tr.find_all("td")] for tr in table.find_all("tr")[1:]]
        df = pd.DataFrame(rows, columns=headers)
        
        # Use the mapping from config
        from .config import COLUMN_MAPPING
        mapped_col = [k for k, v in COLUMN_MAPPING.items() if v == focus_level]
        if not mapped_col: return None
        
        return df[df[mapped_col[0]].str.lower() == state_filter.lower()]
    except Exception as e:
        logging.error(f"Legacy scrape failed: {e}")
        return None
