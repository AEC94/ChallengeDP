# README

## Overview
This repository showcases an Analytics Engineering (AE) exercise intended for an interview assignment. It demonstrates how to ingest raw data, transform it with dbt, and monitor business metrics (such as daily balances) via a Python-based monitoring script. The project is structured to highlight fundamental data engineering and analytics engineering best practices.

Below is a brief overview of each file and its role in the workflow:

### Python Scripts
- **balance_monitor.py**  
  Monitors the daily balances in the DB, potentially sending alerts when certain thresholds or anomalies are detected.

- **data_loading.py**  
  Loads raw data from external sources (e.g., CSV files, APIs) into the DB. This step precedes running any transformations in dbt.

- **dbt_pipeline.py**  
  Orchestrates the dbt workflow (e.g., `dbt run`, `dbt test`) and can be scheduled in a DAG to keep analytics data up to date.

### dbt Models (SQL)
- **stg_organizations.sql**  
  A staging model that standardizes and lightly transforms raw organization data before it’s joined or enriched in subsequent models.

- **stg_invoices.sql**  
  A staging model for invoice data, preparing raw fields for use in downstream reporting and dimensional models.

- **fact_invoices.sql**  
  Core fact table capturing invoice information (e.g., amounts, status, currencies) for further analysis.

- **fact_daily_balance.sql**  
  Fact table providing a daily snapshot of each organization’s balance, enabling time-series analysis of financial positions.

- **dim_organizations.sql**  
  A dimensional table with attributes about each organization (e.g., country code, creation date), serving as a core reference for analytics.

### dbt Configuration (YAML)
- **sources.yml**  
  Defines data sources—for example, the `main` schema along with the `organizations` and `invoices` tables. :contentReference[oaicite:0]{index=0}

- **marts.yml**  
  Describes analytics “marts,” including the `fact_invoices`, `dim_organizations`, and `fact_daily_balance` models. Each column is documented, and dbt tests (like `unique`, `not_null`, and `accepted_values`) are specified to maintain data quality. :contentReference[oaicite:1]{index=1}

## Getting Started

1. **Set Up a Virtual Environment**  
   It’s recommended to use a virtual environment (e.g., `venv` or `conda`) to keep dependencies isolated.

2. **Install Dependencies**  
   - Install Python dependencies (e.g., `dbt-core`, `pandas`, etc.) via `pip`.
   - Ensure the warehouse driver or adapter is properly configured

3. **Configure Database Connection**  
   - Update the `profiles.yml` (in `~/.dbt` directory) to match your DB credentials.

4. **Load Raw Data**  
   - Run `python data_loading.py` to load raw data into the warehouse.

5. **Run dbt**  
   - Execute `dbt build` to run the data models (`stg_organizations.sql`, `stg_invoices.sql`, etc.) and validate data integrity (e.g., `unique` and `not_null` tests for key columns).

6. **Monitor Balances**  
   - Run `python balance_monitor.py` to monitor the daily balances in the warehouse.
