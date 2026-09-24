# 📈 Macro Tracker - Brazilian Macroeconomic Dashboard & Pipeline

An automated data pipeline and dashboard designed to fetch, process, and analyze macroeconomic indicators from Banco Central do Brasil (BCB) and other financial data sources.

---

## 🛠️ Project Architecture

```text
macro_tracker/
├── app/                  # Web interface & components (Dash/Streamlit)
│   ├── components/       # Reusable UI modules
│   └── pages/            # Multi-page views
├── src/                  # Core application engine
│   ├── fetchers/         # Data ingestion scripts (APIs & Scraping)
│   ├── pipeline/         # Data transformation and DB loaders
│   └── reporting/        # Report generators
├── data/                 # Raw/processed data storage
├── reports/              # Generated output files
├── .env                  # Environment secrets (ignored by Git)
├── macro_tracker.db      # SQLite database
└── requirements.txt      # Project dependencies