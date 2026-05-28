# 🇳🇬 Nigeria Polling Unit Data Pipeline
**High-Scale Electoral Data Extraction and Hierarchical Structuring Engine**

[![Python](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Selenium](https://img.shields.io/badge/Automation-Selenium-43A047?style=flat-square&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

## 🔬 Executive Summary
This project implements a robust data engineering pipeline designed to scrape, normalize, and structure electoral administrative hierarchies from the `integrity.ng` platform. The system automates the extraction of the complex State $\rightarrow$ LGA $\rightarrow$ Ward $\rightarrow$ Polling Unit (PU) chain, transforming unstructured HTML data into high-fidelity, analysis-ready datasets for civic auditing and electoral transparency.

### 🏗️ Engineering Challenges Solved
- **Semantic Normalization:** The source data contained systemic labeling errors (e.g., 'LGA' columns containing 'State' names). I implemented a semantic mapping layer in `src/config.py` to programmatically correct these anomalies during extraction.
- **Dynamic State-Space Navigation:** Engineered a recursive Selenium-based scraper that manages dynamic pagination and state-specific filtering across all 37 administrative regions of Nigeria.
- **Relational Data Decomposition:** Developed a processing engine that converts flat scraped lists into a structured relational hierarchy, exported as multi-sheet Excel workbooks for professional auditing.

---

## 📂 Repository Architecture
The project follows a modular data-pipeline pattern to separate extraction logic from data transformation.

```text
├── data/
│   └── raw/               # Immutable raw snapshots of scraped data
├── src/                   # Core Engineering Logic
│   ├── config.py          # Semantic mappings, URL constants, and selectors
│   ├── scraper.py         # Selenium-driven extraction engine
│   ├── processor.py       # Data cleaning and hierarchical Excel generation
│   └── utils.py           # Shared helper functions for data validation
├── experiments/           # Research and Prototyping
│   ├── pagination_test.ipynb       # Page-load and timeout optimization
│   ├── extraction_prototype.ipynb  # Initial selector validation
│   └── prompt_engineering_demo.ipynb # LLM-based data cleaning experiments
└── README.md              # Technical Documentation
```

---

## 🚀 Integration Guide

### 1. Environment Initialization
```bash
git clone https://github.com/Adejare-ml/Nigeria-Polling-Unit-Scraper.git
cd Nigeria-Polling-Unit-Scraper
pip install -r requirements.txt
```

### 2. Pipeline Execution
The pipeline is designed for programmatic execution. Use the following entry point to run the full extraction and processing suite:

```python
from src.scraper import run_full_extraction
from src.processor import DataProcessor

# Stage 1: Extract raw hierarchies
wards, pus = run_full_extraction()

# Stage 2: Process and Generate State-level Audit Reports
processor = DataProcessor()
df_all = processor.process_to_csv(wards, pus)
processor.generate_state_reports(df_all)
```

---

## 🛠 Engineering Stack
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Automation** | Selenium / Webdriver-Manager | Dynamic web interaction and pagination |
| **ETL** | Pandas | Data cleaning, deduplication, and normalization |
| **Storage** | OpenPyXL / CSV | Structured data export for civic auditing |
| **Observability** | Python Logging | System monitoring and error tracking |

---
**Maintainer:** [Adelugba Adejare](https://github.com/Adejare-ml)
