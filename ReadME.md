# PostgreSQL SQL Guide for This Repository

This guide helps you:

1. Create PostgreSQL tables for each dataset in this repo.
2. Load data using SQL-friendly workflows (`COPY`, JSON expansion, staging tables).
3. Practice SQL with **30 curated questions** (basic → advanced).

---

## 1) Datasets in this repository

- `Global_Superstore2.csv`
- `data_engineer_salaries.csv`
- `users.json`
- `german_cars_dataset.json`
- `excel_sales_project.xlsx` (sheet: `Sales Data`)
- `supermarket_transactions.csv.xlsx` (sheet: `supermarket_transactions`)

---

## 2) Create a database and schema

```sql
-- Run as a PostgreSQL superuser or user with CREATE DATABASE privilege.
CREATE DATABASE data_practice;
\c data_practice;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;
```

---

## 3) Table creation SQL (DDL)

## 3.1 Global Superstore (`Global_Superstore2.csv`)

```sql
CREATE TABLE IF NOT EXISTS raw.global_superstore (
    row_id               INTEGER PRIMARY KEY,
    order_id             TEXT NOT NULL,
    order_date           DATE,
    ship_date            DATE,
    ship_mode            TEXT,
    customer_id          TEXT,
    customer_name        TEXT,
    segment              TEXT,
    city                 TEXT,
    state                TEXT,
    country              TEXT,
    postal_code          TEXT,
    market               TEXT,
    region               TEXT,
    product_id           TEXT,
    category             TEXT,
    sub_category         TEXT,
    product_name         TEXT,
    sales                NUMERIC(14,2),
    quantity             INTEGER,
    discount             NUMERIC(6,3),
    profit               NUMERIC(14,4),
    shipping_cost        NUMERIC(14,2),
    order_priority       TEXT
);
```

## 3.2 Data Engineer Salaries (`data_engineer_salaries.csv`)

```sql
CREATE TABLE IF NOT EXISTS raw.data_engineer_salaries (
    region               TEXT,
    country              TEXT,
    level                TEXT,
    min_salary_usd       INTEGER,
    avg_salary_usd       INTEGER,
    max_salary_usd       INTEGER,
    notes                TEXT,
    CONSTRAINT salaries_level_check CHECK (level IN ('Junior', 'Mid-Level', 'Senior')),
    CONSTRAINT salaries_range_check CHECK (min_salary_usd <= avg_salary_usd AND avg_salary_usd <= max_salary_usd)
);
```

## 3.3 Users (`users.json`)

```sql
CREATE TABLE IF NOT EXISTS raw.users (
    id                   INTEGER PRIMARY KEY,
    name                 TEXT NOT NULL,
    email                TEXT UNIQUE,
    city                 TEXT,
    phone                TEXT
);
```

## 3.4 German Cars (`german_cars_dataset.json`)

```sql
CREATE TABLE IF NOT EXISTS raw.german_cars (
    car_id               BIGSERIAL PRIMARY KEY,
    brand                TEXT NOT NULL,
    model                TEXT NOT NULL,
    year                 INTEGER,
    engine               TEXT,
    horsepower           INTEGER,
    transmission         TEXT,
    fuel_type            TEXT,
    price_usd            NUMERIC(12,2)
);
```

## 3.5 Excel Sales Project (`excel_sales_project.xlsx`, sheet `Sales Data`)

```sql
CREATE TABLE IF NOT EXISTS raw.excel_sales_data (
    order_id             TEXT,
    customer_id          TEXT,
    customer_name        TEXT,
    region               TEXT,
    product              TEXT,
    product_category     TEXT,
    quantity_sold        INTEGER,
    unit_price           NUMERIC(12,2),
    discount_pct         NUMERIC(6,2),
    sales_rep            TEXT,
    payment_method       TEXT,
    shipping_cost        NUMERIC(12,2),
    order_date           DATE,
    sales_date           DATE,
    customer_age         INTEGER,
    product_rating       NUMERIC(4,2),
    total_sales          NUMERIC(14,2),
    region_sales_total   NUMERIC(14,2),
    order_status         TEXT,
    return_status        TEXT,
    customer_feedback    TEXT,
    supplier             TEXT,
    quantity_in_stock    INTEGER
);
```

## 3.6 Supermarket Transactions (`supermarket_transactions.csv.xlsx`, sheet `supermarket_transactions`)

```sql
CREATE TABLE IF NOT EXISTS raw.supermarket_transactions (
    id                   TEXT,
    timestamp_raw        TEXT,
    quantity             TEXT,
    product_id           TEXT,
    product_name         TEXT,
    unit_price           TEXT,
    total_amount         TEXT,
    store                TEXT,
    payment_method       TEXT,
    customer_id          TEXT,
    customer_type        TEXT
);
```

---

## 4) Insert/load data into PostgreSQL

> Tip: For `.xlsx` files, export each sheet to CSV first (Excel/LibreOffice) or use Python to convert.

## 4.1 Load CSV files with `COPY`

```sql
-- Adjust absolute paths for your machine/container.
COPY raw.global_superstore
FROM '/workspace/Data/Global_Superstore2.csv'
WITH (FORMAT csv, HEADER true);

COPY raw.data_engineer_salaries
FROM '/workspace/Data/data_engineer_salaries.csv'
WITH (FORMAT csv, HEADER true);
```

## 4.2 Load JSON arrays using `jsonb_to_recordset`

```sql
-- users.json
WITH src AS (
    SELECT pg_read_file('/workspace/Data/users.json')::jsonb AS j
)
INSERT INTO raw.users (id, name, email, city, phone)
SELECT *
FROM jsonb_to_recordset((SELECT j FROM src)) AS x(
    id INTEGER,
    name TEXT,
    email TEXT,
    city TEXT,
    phone TEXT
);

-- german_cars_dataset.json
WITH src AS (
    SELECT pg_read_file('/workspace/Data/german_cars_dataset.json')::jsonb AS j
)
INSERT INTO raw.german_cars (brand, model, year, engine, horsepower, transmission, fuel_type, price_usd)
SELECT *
FROM jsonb_to_recordset((SELECT j FROM src)) AS x(
    brand TEXT,
    model TEXT,
    year INTEGER,
    engine TEXT,
    horsepower INTEGER,
    transmission TEXT,
    fuel_type TEXT,
    price_usd NUMERIC(12,2)
);
```

## 4.3 Load converted Excel sheets (CSV export)

Export these files first:

- `excel_sales_data.csv` (from sheet `Sales Data`)
- `supermarket_transactions.csv` (from sheet `supermarket_transactions`)

Then run:

```sql
COPY raw.excel_sales_data
FROM '/workspace/Data/excel_sales_data.csv'
WITH (FORMAT csv, HEADER true);

-- For this sheet, load as text first, then clean in analytics layer.
-- (Useful because source appears to have shifted/mixed types.)
COPY raw.supermarket_transactions (
    id, timestamp_raw, quantity, product_id, product_name,
    unit_price, total_amount, store, payment_method, customer_id, customer_type
)
FROM '/workspace/Data/supermarket_transactions.csv'
WITH (FORMAT csv, HEADER true);
```

> ⚠️ The supermarket sheet appears misaligned in raw form (IDs and fields shifted). Keep this table as text and build a cleaned view/table after data profiling.

---

## 5) Good SQL habits (quick checklist)

- Use `snake_case` names for tables/columns.
- Define data types carefully (`DATE`, `TIMESTAMP`, `NUMERIC`).
- Add constraints (`PRIMARY KEY`, `UNIQUE`, `CHECK`) where possible.
- Use staging tables for messy source files.
- Use `NULLIF(col, '')` when casting text imports.
- Validate loaded data with row counts and sanity checks.

Example validation SQL:

```sql
SELECT 'global_superstore' AS table_name, COUNT(*) FROM raw.global_superstore
UNION ALL
SELECT 'data_engineer_salaries', COUNT(*) FROM raw.data_engineer_salaries
UNION ALL
SELECT 'users', COUNT(*) FROM raw.users
UNION ALL
SELECT 'german_cars', COUNT(*) FROM raw.german_cars
UNION ALL
SELECT 'excel_sales_data', COUNT(*) FROM raw.excel_sales_data
UNION ALL
SELECT 'supermarket_transactions', COUNT(*) FROM raw.supermarket_transactions;
```

---

## 6) 30 SQL practice questions (curated)

## A. Foundations (1–10)

1. List all columns from `raw.users`.
2. Count total users by city.
3. Show all German cars sorted by `price_usd` descending.
4. Find the top 10 orders by `sales` in `raw.global_superstore`.
5. Count salary records per `level`.
6. Get distinct `payment_method` values from `raw.excel_sales_data`.
7. Find all superstore orders with negative `profit`.
8. Show users whose email ends with `example.com`.
9. Calculate average `horsepower` per `brand`.
10. Return all salary rows where `avg_salary_usd` is above 120000.

## B. Filtering + Aggregation (11–20)

11. Total `sales` by `region` in `raw.global_superstore`.
12. Total `profit` by `category` and `sub_category`.
13. Average `discount_pct` by `region` in `raw.excel_sales_data`.
14. Sum `total_sales` by `sales_rep`.
15. Count cars by `fuel_type` and `transmission`.
16. Find salary spread (`max_salary_usd - min_salary_usd`) per country.
17. Top 5 customers by sales in superstore.
18. Monthly sales trend from `raw.excel_sales_data` using `date_trunc('month', sales_date)`.
19. Average product rating by `product` where rating is not null.
20. Number of returned orders by region (`return_status='Returned'`).

## C. Joins + CTEs + Windows (21–30)

21. Join `raw.users` with `raw.excel_sales_data` (by customer name approximation) and count orders per user.
22. Rank superstore products by total sales within each category (window `RANK()`).
23. Compute running monthly sales total for each region.
24. Find the 3 most profitable products per market (window partitioned by market).
25. Use a CTE to classify superstore orders into `loss`, `low`, `medium`, `high` profitability bands.
26. Build a cohort query: first purchase month per customer in `raw.excel_sales_data`.
27. Detect duplicate users by email and show counts.
28. Compare each country’s `avg_salary_usd` to global average using window functions.
29. Compute contribution percentage of each sub-category to category sales.
30. Create a view `analytics.vw_sales_kpi` with KPIs: total sales, total profit, avg discount, return rate.

---

## 7) Bonus: ready-to-run sample answers (3 examples)

```sql
-- Q11: Total sales by region (superstore)
SELECT region, ROUND(SUM(sales), 2) AS total_sales
FROM raw.global_superstore
GROUP BY region
ORDER BY total_sales DESC;

-- Q22: Rank products by total sales within category
WITH product_sales AS (
    SELECT category, product_name, SUM(sales) AS total_sales
    FROM raw.global_superstore
    GROUP BY category, product_name
)
SELECT
    category,
    product_name,
    total_sales,
    RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) AS sales_rank
FROM product_sales;

-- Q28: salary country vs global average
SELECT
    country,
    ROUND(AVG(avg_salary_usd), 2) AS country_avg,
    ROUND(AVG(AVG(avg_salary_usd)) OVER (), 2) AS global_avg,
    ROUND(AVG(avg_salary_usd) - AVG(AVG(avg_salary_usd)) OVER (), 2) AS delta_vs_global
FROM raw.data_engineer_salaries
GROUP BY country
ORDER BY delta_vs_global DESC;
```

---

If you want, next step can be a **`schema.sql` + `load.sql` + `practice.sql` split** so you can run everything in one command with `psql -f`.
