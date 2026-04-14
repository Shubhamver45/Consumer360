# Consumer360 - Customer Segmentation & CLV Engine

This project contains the complete production-grade backend and analytics engine for the **Consumer360 Retail Analytics Dashboard**.

## Overview
Consumer360 targets generic marketing problems by providing instantaneous customer segmenting ("Champions" vs "Churn Risks"), detailed market basket logic, cohort retention, and predictive Customer Lifetime Value (CLV).

## Architecture Details
- **Data Engineering (SQL/Supabase):**
  Raw transaction logs are cleansed, standardized, and modeled into a Star Schema (`Fact_Sales`, `Dim_Customer`, `Dim_Product`) utilizing strict indexing so queries run well under ~2 seconds. Views are provided for direct Power BI consumption.
- **The Logic Core (Python):**
  - **RFM Analysis:** Custom 5x5 matrix scoring Recency, Frequency, and Monetary to classify customers into exact actionable segments.
  - **Market Basket (Association Rules):** Identifies highly correlated products using the Apriori algorithm via `mlxtend`.
  - **Cohort Analysis:** Tracks customer retention over explicit months following their first signup.
  - **Predictive CLV (`lifetimes`):** Fits BG/NBD and Gamma-Gamma statistical models to mathematically predict churn risk ("Probability Alive") and future lifetime value.

## Quick Start (Local & DB)

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Supabase / Database Configuration (Week 1):**
   - Head over to your Supabase project's SQL editor.
   - Execute script `sql/01_raw_schema.sql` to prepare the landing table.
   - Execute `sql/02_cleaning_and_star_schema.sql` to normalize data.
   - Execute `sql/03_analytical_queries.sql` to establish Power BI Views.
   - Duplicate `.env.example` as `.env` and assign your connection details.

3. **Data Download:**
   If you have a fresh environment without data, download the real-world e-commerce dataset first!
   ```bash
   python download_real_data.py
   ```
   *(This outputs `raw_transaction_logs.csv` which you can upload into your Supabase `raw_transactions` table).*

4. **The Weekly Automation Job (Week 2):**
   Execute the heavy analytical Python pipeline. This is designed to be an automated weekly process.
   ```bash
   python main.py
   ```
   *Note: If no database connection is found, the script will gracefully fallback to generating mock data in-memory and running the complete logic anyway so you can test it immediately.*

All results are compiled into the `/output` folder as clean flat files, instantly ready for Power BI dashboard consumption!
