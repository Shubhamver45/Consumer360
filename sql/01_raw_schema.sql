-- Raw transactions landing table.
-- Designed to ingest dirty CSV logs prior to cleaning.

CREATE TABLE IF NOT EXISTS raw_transactions (
    id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50),
    stock_code VARCHAR(50),
    description VARCHAR(255),
    quantity VARCHAR(50),      -- Varchar to catch bad data natively
    invoice_date VARCHAR(100), -- Varchar to prevent copy errors
    unit_price VARCHAR(50),    -- Varchar to catch currency symbols/bad formats
    customer_id VARCHAR(50),
    country VARCHAR(100)
);
