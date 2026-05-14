# Project Configuration

NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", 
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", 
    "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", 
    "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", 
    "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT"
]

MAX_PAGES = 200
BASE_URL = "https://integrity.ng/index.php"
WARDS_URL = f"{BASE_URL}/wards/browse"
UNITS_URL = f"{BASE_URL}/units/browse"

# Mapping to handle source data inconsistencies (mislabeled columns)
COLUMN_MAPPING = {
    "LGA": "State",
    "Ward": "LGA",
    "Polling Unit": "Ward"
}
