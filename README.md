# Nigeria Electoral Data Pipeline

A professional data engineering pipeline designed to extract, clean, and structure polling unit data from the INEC-integrated integrity.ng platform.

## 🚀 Project Overview

This project automates the extraction of electoral administrative hierarchies (State $\rightarrow$ LGA $\rightarrow$ Ward $\rightarrow$ Polling Unit) from web sources. It transforms unstructured HTML table data into a clean, analysis-ready format, providing both comprehensive CSV datasets and state-specific Excel reports for auditing and civic tech applications.

### Key Technical Challenges Solved:
- **Data Normalization:** Implemented a mapping layer to correct systemic mislabeling in the source website's columns (where 'LGA' often represented 'State', etc.).
- **Pagination Handling:** Engineered a robust Selenium-based scraper that handles dynamic pagination and state-based filtering across 37 administrative regions.
- **Hierarchical Structuring:** Developed a processing engine that decomposes flat data into a multi-level relational structure exported to multi-sheet Excel workbooks.

## 🛠 Tech Stack

- **Language:** Python 3.x
- **Libraries:** 
  - `Selenium` & `Webdriver-Manager` (Web Automation)
  - `Pandas` (Data Manipulation & Cleaning)
  - `OpenPyXL` (Excel Engine)
  - `Logging` (System Monitoring)

## 📁 Project Structure

```text
├── data/
│   ├── raw/            # Original scraped snapshots
│   └── processed/     # Cleaned CSVs and State-level Excel reports
├── src/
│   ├── config.py       # Constants, URLS, and Column Mappings
│   ├── scraper.py      # Selenium-based extraction logic
│   └── processor.py    # Data cleaning and Excel generation
├── notebooks/          # Exploratory data analysis and prototype runs
└── README.md           # Project documentation
```

## 🚦 Getting Started

### Prerequisites
- Chrome Browser installed.
- Python 3.8+

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install pandas selenium webdriver-manager openpyxl
   ```

### Execution
To run the full pipeline:
```python
from src.scraper import run_full_extraction
from src.processor import DataProcessor

# 1. Extract
wards, pus = run_full_extraction()

# 2. Process & Export
processor = DataProcessor()
df_all = processor.process_to_csv(wards, pus)
processor.generate_state_reports(df_all)
```

## 📊 Output Format
Each state generates a dedicated `.xlsx` report with the following structure:
- **State_LGA**: Unique State and LGA pairings.
- **LGA_Wards**: Administrative breakdown of Wards per LGA.
- **LGA_Wards_PUs**: The most granular level, mapping every Polling Unit to its respective Ward and LGA.
