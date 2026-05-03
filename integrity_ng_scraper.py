
"""
Detailed Documentation of the LGAs, Wards, and Polling Units Scraper

Objective:
This script collects Local Government Areas (LGAs), Wards, and Polling Units (PUs) 
for all 36 Nigerian states and the FCT from integrity.ng and saves them in CSV files.

Author: Python Electoral Data Scraper
Date: 2025
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# List of all Nigerian states and FCT
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", 
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", 
    "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", 
    "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", 
    "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT"
]

# Maximum pages to scrape (adjust if needed)
MAX_PAGES = 200

def init_driver():
    """
    Initialize Chrome WebDriver using webdriver-manager
    """
    try:
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        # Remove headless mode for debugging (add back for production)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("Chrome driver initialized successfully!")
        return driver

    except Exception as e:
        print(f"Error initializing driver: {e}")
        return None

def fetch_lgas_and_wards(driver, state_name):
    """
    Fetch LGAs and Wards for a specific state from the wards page

    Args:
        driver: Selenium WebDriver instance
        state_name: Name of the Nigerian state

    Returns:
        List of tuples: [(state, lga, ward), ...]
    """
    wards_data = []
    seen_entries = set()  # To avoid duplicates

    print(f"\nScraping wards for {state_name}...")

    try:
        # Navigate to wards page
        driver.get("https://integrity.ng/index.php/wards/browse")
        time.sleep(3)

        page_num = 1

        while page_num <= MAX_PAGES:
            try:
                print(f"  Processing page {page_num}...")

                # Wait for table to load
                wait = WebDriverWait(driver, 10)
                table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

                # Find all rows in the table body
                rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

                if not rows:
                    print(f"  No rows found on page {page_num}")
                    break

                page_has_state_data = False

                # Process each row
                for row in rows:
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= 3:  # Assuming State, LGA, Ward columns
                            row_state = cells[0].text.strip()
                            row_lga = cells[1].text.strip()
                            row_ward = cells[2].text.strip()

                            # Check if this row belongs to our target state
                            if row_state.lower() == state_name.lower():
                                entry = (row_state, row_lga, row_ward)
                                entry_key = f"{row_state}|{row_lga}|{row_ward}"

                                if entry_key not in seen_entries:
                                    wards_data.append(entry)
                                    seen_entries.add(entry_key)
                                    page_has_state_data = True

                    except Exception as row_error:
                        print(f"    Error processing row: {row_error}")
                        continue

                # Try to go to next page
                try:
                    next_button = driver.find_element(By.LINK_TEXT, "Next")
                    if next_button and next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)
                        page_num += 1
                    else:
                        print(f"  No more pages available")
                        break
                except NoSuchElementException:
                    print(f"  Next button not found, stopping pagination")
                    break

            except TimeoutException:
                print(f"  Timeout on page {page_num}")
                break
            except Exception as page_error:
                print(f"  Error on page {page_num}: {page_error}")
                break

    except Exception as e:
        print(f"Error fetching wards for {state_name}: {e}")

    print(f"  Found {len(wards_data)} wards for {state_name}")
    return wards_data

def fetch_polling_units(driver, state_name):
    """
    Fetch Polling Units for a specific state from the polling units page

    Args:
        driver: Selenium WebDriver instance
        state_name: Name of the Nigerian state

    Returns:
        List of tuples: [(state, lga, ward, polling_unit), ...]
    """
    pus_data = []
    seen_entries = set()  # To avoid duplicates

    print(f"\nScraping polling units for {state_name}...")

    try:
        # Navigate to polling units page
        driver.get("https://integrity.ng/index.php/units/browse")
        time.sleep(3)

        page_num = 1

        while page_num <= MAX_PAGES:
            try:
                print(f"  Processing page {page_num}...")

                # Wait for table to load
                wait = WebDriverWait(driver, 10)
                table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

                # Find all rows in the table body
                rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

                if not rows:
                    print(f"  No rows found on page {page_num}")
                    break

                # Process each row
                for row in rows:
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= 4:  # Assuming State, LGA, Ward, PU columns
                            row_state = cells[0].text.strip()
                            row_lga = cells[1].text.strip()
                            row_ward = cells[2].text.strip()
                            row_pu = cells[3].text.strip()

                            # Check if this row belongs to our target state
                            if row_state.lower() == state_name.lower():
                                entry = (row_state, row_lga, row_ward, row_pu)
                                entry_key = f"{row_state}|{row_lga}|{row_ward}|{row_pu}"

                                if entry_key not in seen_entries:
                                    pus_data.append(entry)
                                    seen_entries.add(entry_key)

                    except Exception as row_error:
                        print(f"    Error processing row: {row_error}")
                        continue

                # Try to go to next page
                try:
                    next_button = driver.find_element(By.LINK_TEXT, "Next")
                    if next_button and next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)
                        page_num += 1
                    else:
                        print(f"  No more pages available")
                        break
                except NoSuchElementException:
                    print(f"  Next button not found, stopping pagination")
                    break

            except TimeoutException:
                print(f"  Timeout on page {page_num}")
                break
            except Exception as page_error:
                print(f"  Error on page {page_num}: {page_error}")
                break

    except Exception as e:
        print(f"Error fetching polling units for {state_name}: {e}")

    print(f"  Found {len(pus_data)} polling units for {state_name}")
    return pus_data

def save_all_to_csv(all_wards, all_pus):
    """
    Save all collected data to three separate CSV files

    Args:
        all_wards: List of ward data tuples
        all_pus: List of polling unit data tuples
    """
    try:
        print("\nSaving data to CSV files...")

        # Create DataFrame for wards
        wards_df = pd.DataFrame(all_wards, columns=['State', 'LGA', 'Ward'])

        # Create DataFrame for polling units
        pus_df = pd.DataFrame(all_pus, columns=['State', 'LGA', 'Ward', 'Polling Unit'])

        # Extract unique LGAs from wards data
        lgas_df = wards_df[['State', 'LGA']].drop_duplicates().sort_values(['State', 'LGA'])

        # Save to CSV files
        lgas_df.to_csv('All_LGAs.csv', index=False)
        print(f"  Saved {len(lgas_df)} unique LGAs to All_LGAs.csv")

        wards_df.to_csv('All_LGA_Wards.csv', index=False)
        print(f"  Saved {len(wards_df)} wards to All_LGA_Wards.csv")

        pus_df.to_csv('All_Wards_PUs.csv', index=False)
        print(f"  Saved {len(pus_df)} polling units to All_Wards_PUs.csv")

        # Display summary
        print("\n=== SCRAPING SUMMARY ===")
        print(f"Total States Processed: {len(lgas_df['State'].unique())}")
        print(f"Total LGAs: {len(lgas_df)}")
        print(f"Total Wards: {len(wards_df)}")
        print(f"Total Polling Units: {len(pus_df)}")
        print("=== FILES CREATED ===")
        print("1. All_LGAs.csv")
        print("2. All_LGA_Wards.csv") 
        print("3. All_Wards_PUs.csv")

    except Exception as e:
        print(f"Error saving to CSV: {e}")

def run_all_states():
    """
    Main function to run the scraper for all Nigerian states
    """
    print("Starting LGAs, Wards, and Polling Units Scraper for All Nigerian States")
    print("=" * 70)

    # Initialize driver
    driver = init_driver()
    if not driver:
        print("Failed to initialize driver. Exiting...")
        return

    all_wards = []
    all_pus = []

    try:
        for state in NIGERIAN_STATES:
            print(f"\n{'='*50}")
            print(f"Processing: {state}")
            print(f"{'='*50}")

            # Fetch wards for this state
            wards = fetch_lgas_and_wards(driver, state)
            all_wards.extend(wards)

            # If we found wards, also fetch polling units
            if wards:
                pus = fetch_polling_units(driver, state)
                all_pus.extend(pus)
            else:
                print(f"  No wards found for {state}, skipping polling units")

            # Small delay between states
            time.sleep(1)

        # Save all collected data
        save_all_to_csv(all_wards, all_pus)

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        if all_wards or all_pus:
            print("Saving partial data...")
            save_all_to_csv(all_wards, all_pus)

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if all_wards or all_pus:
            print("Saving partial data...")
            save_all_to_csv(all_wards, all_pus)

    finally:
        # Close the driver
        if driver:
            driver.quit()
            print("\nBrowser closed successfully")

# Main execution
if __name__ == "__main__":
    print(__doc__)

    # Ask for confirmation before starting
    response = input("\nThis will scrape data from integrity.ng. Continue? (y/n): ")
    if response.lower() in ['y', 'yes']:
        run_all_states()
    else:
        print("Scraping cancelled by user.")
        
