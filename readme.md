# README

## Overview
This repository showcases an Analytics Engineering (AE) exercise intended for an interview assignment. It demonstrates how to ingest raw data, transform it with dbt, and monitor business metrics (such as daily balances) via a Python-based monitoring script. The project is structured to highlight fundamental data engineering and analytics engineering best practices.

Below is a brief overview of each file and its role in the workflow:

### Python Scripts
- **balance_monitor.py**  
  Monitors the daily balances in your data warehouse, potentially sending alerts when certain thresholds or anomalies are detected.

- **data_loading.py**  
  Loads raw data from external sources (e.g., CSV files, APIs) into your data warehouse. This step precedes running any transformations in dbt.

- **dbt_pipeline.py**  
  Orchestrates the dbt workflow (e.g., `dbt run`, `dbt test`) and can be scheduled in a CI/CD pipeline or a cron job to keep analytics data up to date.

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
  Defines your data sources—for example, the `main` schema along with the `organizations` and `invoices` tables. :contentReference[oaicite:0]{index=0}

- **marts.yml**  
  Describes your analytics “marts,” including the `fact_invoices`, `dim_organizations`, and `fact_daily_balance` models. Each column is documented, and dbt tests (like `unique`, `not_null`, and `accepted_values`) are specified to maintain data quality. :contentReference[oaicite:1]{index=1}

## Project Structure
A common structure for your project might look like this:

