-- =========================================================
-- Step 1: Create Production Star Schema Tables
-- =========================================================
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;

CREATE TABLE dim_customer (
    customer_id INTEGER PRIMARY KEY,
    country VARCHAR(100),
    signup_date DATE
);
-- Optimize aggregation by geography
CREATE INDEX idx_dim_customer_country ON dim_customer(country);

CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    stock_code VARCHAR(50) UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE fact_sales (
    transaction_id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50),
    customer_id INTEGER REFERENCES dim_customer(customer_id),
    product_id INTEGER REFERENCES dim_product(product_id),
    quantity INTEGER,
    unit_price NUMERIC(10, 2),
    total_amount NUMERIC(10, 2),
    transaction_date TIMESTAMP
);
-- Accelerate time-series filtering
CREATE INDEX idx_fact_sales_date ON fact_sales(transaction_date);
-- Accelerate customer aggregations
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);

-- =========================================================
-- Step 2: Cleanse and Load Data into Star Schema
-- =========================================================

-- Populate Dim_Customer
INSERT INTO dim_customer (customer_id, country, signup_date)
SELECT 
    CAST(CAST(customer_id AS NUMERIC) AS INTEGER), 
    COALESCE(MAX(country), 'Unknown'),
    MIN(CAST(invoice_date AS DATE))
FROM raw_transactions
WHERE customer_id IS NOT NULL AND customer_id != ''
GROUP BY CAST(CAST(customer_id AS NUMERIC) AS INTEGER)
ON CONFLICT (customer_id) DO NOTHING;

-- Populate Dim_Product
INSERT INTO dim_product (stock_code, description)
SELECT 
    stock_code, 
    MAX(description)
FROM raw_transactions
WHERE stock_code IS NOT NULL
GROUP BY stock_code
ON CONFLICT (stock_code) DO NOTHING;

-- Populate Fact_Sales (Standardizing NULLs, Data Types, and removing anomalies)
INSERT INTO fact_sales (invoice_no, customer_id, product_id, quantity, unit_price, total_amount, transaction_date)
SELECT 
    r.invoice_no,
    CAST(CAST(r.customer_id AS NUMERIC) AS INTEGER),
    p.product_id,
    CAST(CAST(r.quantity AS NUMERIC) AS INTEGER),
    CAST(CAST(r.unit_price AS NUMERIC) AS NUMERIC(10, 2)),
    CAST(CAST(r.quantity AS NUMERIC) AS INTEGER) * CAST(CAST(r.unit_price AS NUMERIC) AS NUMERIC(10, 2)),
    CAST(r.invoice_date AS TIMESTAMP)
FROM raw_transactions r
JOIN dim_product p ON r.stock_code = p.stock_code
WHERE r.customer_id IS NOT NULL 
  AND r.customer_id != ''
  -- Identify and remove data anomalies
  AND r.quantity IS NOT NULL 
  AND r.quantity ~ '^[0-9\.\-]+$' -- Ensure it matches numbers with decimals or negatives
  AND CAST(CAST(r.quantity AS NUMERIC) AS INTEGER) > 0 
  AND r.unit_price IS NOT NULL
  AND r.invoice_date != 'invalid_date';
