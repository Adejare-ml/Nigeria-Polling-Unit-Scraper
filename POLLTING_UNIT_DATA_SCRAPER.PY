import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_polling_data(
    url: str,
    focus_level: str,
    state_filter: str,
    description: str = ""
):
    """
    Scrape and filter polling unit data from a given INEC-integrated website.

    Parameters:
        url (str): The webpage URL containing the data (e.g. wards, LGAs, polling units).
        focus_level (str): One of 'State', 'LGA', or 'Ward'. Determines which column to focus on.
        state_filter (str): The specific state to scrape.
        description (str): Optional. A short description of what you're trying to extract or analyze.

    Returns:
        pd.DataFrame: Filtered dataset based on the state and focus level.
    """

    print(f"\n📄 Description: {description}")
    print(f"🔗 Fetching data from: {url} ...")

    try:
        # Fetch and parse
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse HTML table (assumes the first one on the page)
        table = soup.find("table")
        if not table:
            print("❌ No table found on the page.")
            return None

        headers = [th.text.strip() for th in table.find_all("th")]
        rows = [
            [td.text.strip() for td in tr.find_all("td")]
            for tr in table.find_all("tr")[1:]  # Skip header
        ]

        df = pd.DataFrame(rows, columns=headers)

        # Standardize and clean column names
        df.columns = [col.strip() for col in df.columns]
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()

        # Apply filtering based on INEC mislabeling caveat
        column_mapping = {
            "LGA": "State",
            "Ward": "LGA",
            "Polling Unit": "Ward"
        }

        # Use remapped column
        if focus_level not in ["State", "LGA", "Ward"]:
            print("❌ Invalid focus_level. Use 'State', 'LGA', or 'Ward'.")
            return None

        mapped_column = [k for k, v in column_mapping.items() if v == focus_level]
        if not mapped_column:
            print("❌ Could not resolve focus level based on known INEC structure.")
            return None

        focus_column = mapped_column[0]
        df_filtered = df[df[focus_column].str.lower() == state_filter.strip().lower()]

        print(f"✅ Found {len(df_filtered)} rows for {focus_level}: '{state_filter}'")
        return df_filtered

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None


## EXAMPLE USAGE 

## # Example: Scrape wards for Kano state
#result = scrape_polling_data(
#    url="https://integrity.ng/index.php/wards/browse",
#    focus_level="LGA",
#    state_filter="Kano",
#    description="Extract all Wards under Kano state from INEC-integrity website."
#)

# Save if result is valid
#if result is not None:
#    result.to_csv("kano_wards.csv", index=False)
