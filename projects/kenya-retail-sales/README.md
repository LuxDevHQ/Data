# Kenya Retail Sales — JSON, SQL and Power BI Project Brief

**Dataset:** [`kenya_retail_sales.json`](../../datasets/json/kenya_retail_sales.json) · 80 orders · 199 order items · 12 customers · 10 products · 5 Jan 2026 → 28 Jul 2026 · Currency: KES

You are a data analyst for a Kenyan omnichannel retailer. Management wants a reliable
relational model and a dashboard that explain sales performance, customer behaviour,
product demand, discounts, payments, and delivery operations. The source is nested JSON,
so the first part of the project is to inspect and normalize it before doing any analysis.

The data is synthetic and suitable for practice. Keep the source JSON unchanged and make
your transformation reproducible.

---

## Project tools

- Python 3 with `json` or pandas for inspecting and flattening the source
- PostgreSQL and DBeaver for relational modelling and SQL analysis
- Power BI Desktop for the final dashboard

---

## Source structure

The root object contains dataset metadata and an `orders` array. Each order contains:

- one nested `customer` object;
- one nested `shipping` object;
- one nested `payment` object; and
- an `items` array containing one or more order-item objects.

This means one JSON order must not be loaded directly into one flat table: repeating the
order, customer, and payment fields for every item would introduce duplication and make
updates unreliable.

### Getting started in Python

```python
import json
from pathlib import Path

path = Path("../../datasets/json/kenya_retail_sales.json")
with path.open(encoding="utf-8") as file:
    retail = json.load(file)

orders = retail["orders"]
print(len(orders))
print(orders[0].keys())
```

If your notebook is stored somewhere else, adjust the relative path rather than moving or
editing the source file.

---

## Recommended relational model

Normalize the JSON into five tables. Use the IDs—not names—as join keys, and store all
money fields as `NUMERIC(14,2)` so calculations do not depend on floating-point rounding.

### `customers`

| Column | Type | Description |
|---|---|---|
| `customer_id` | text, primary key | Unique customer ID |
| `name` | text | Customer name |
| `gender` | text | Customer gender |
| `age` | integer | Age in years |
| `city` | text | Customer's home city |
| `segment` | text | Consumer, Corporate, or Small Business |

### `products`

| Column | Type | Description |
|---|---|---|
| `product_id` | text, primary key | Unique product ID |
| `product_name` | text | Product description |
| `category` | text | Product category |
| `unit_price` | numeric | Catalogue unit price in KES |

### `orders`

| Column | Type | Description |
|---|---|---|
| `order_id` | text, primary key | Unique order ID |
| `order_date` | date | Date the order was placed |
| `customer_id` | text, foreign key | Links to `customers` |
| `sales_channel` | text | Mobile App, Physical Store, or Website |
| `status` | text | Completed, Cancelled, or Pending |
| `shipping_city` | text | Delivery destination |
| `delivery_fee` | numeric | Delivery fee in KES |
| `delivery_days` | integer | Recorded delivery duration |
| `subtotal` | numeric | Sum of discounted item totals |
| `order_total` | numeric | Subtotal plus delivery fee |

### `order_items`

| Column | Type | Description |
|---|---|---|
| `order_item_id` | text, primary key | Unique line-item ID |
| `order_id` | text, foreign key | Links to `orders` |
| `product_id` | text, foreign key | Links to `products` |
| `quantity` | integer | Units ordered |
| `unit_price` | numeric | Unit price captured at purchase time |
| `discount_pct` | numeric | Percentage discount on the line |
| `line_total` | numeric | Quantity × unit price after discount |

### `payments`

| Column | Type | Description |
|---|---|---|
| `payment_id` | text, primary key | Unique payment ID |
| `order_id` | text, unique foreign key | Links one payment to one order |
| `payment_method` | text | Card, M-Pesa, or Bank Transfer |
| `payment_status` | text | Paid, Refunded, or Pending |
| `amount` | numeric | Payment amount in KES |

### Relationships

```text
customers 1 ───< orders 1 ───< order_items >─── 1 products
                    │
                    └──── 1 payments
```

- One customer can place many orders.
- One order can contain many order items.
- One product can appear in many order items.
- Each order has one payment record in this dataset.

---

## PostgreSQL setup

Create a database named `kenya_retail_sales_db`, then create the tables in dependency
order so every foreign key points to an existing parent table.

```sql
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    gender      TEXT,
    age         INTEGER CHECK (age > 0),
    city        TEXT,
    segment     TEXT
);

CREATE TABLE products (
    product_id   TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    unit_price   NUMERIC(14,2) NOT NULL CHECK (unit_price >= 0)
);

CREATE TABLE orders (
    order_id      TEXT PRIMARY KEY,
    order_date    DATE NOT NULL,
    customer_id   TEXT NOT NULL REFERENCES customers(customer_id),
    sales_channel TEXT NOT NULL,
    status        TEXT NOT NULL,
    shipping_city TEXT,
    delivery_fee  NUMERIC(14,2) NOT NULL CHECK (delivery_fee >= 0),
    delivery_days INTEGER CHECK (delivery_days >= 0),
    subtotal      NUMERIC(14,2) NOT NULL CHECK (subtotal >= 0),
    order_total   NUMERIC(14,2) NOT NULL CHECK (order_total >= 0)
);

CREATE TABLE order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id      TEXT NOT NULL REFERENCES orders(order_id),
    product_id    TEXT NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(14,2) NOT NULL CHECK (unit_price >= 0),
    discount_pct  NUMERIC(5,2) NOT NULL CHECK (discount_pct BETWEEN 0 AND 100),
    line_total    NUMERIC(14,2) NOT NULL CHECK (line_total >= 0)
);

CREATE TABLE payments (
    payment_id     TEXT PRIMARY KEY,
    order_id       TEXT NOT NULL UNIQUE REFERENCES orders(order_id),
    payment_method TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    amount         NUMERIC(14,2) NOT NULL CHECK (amount >= 0)
);
```

Write a Python script that extracts distinct customers and products, then loads parents
before children in this order: `customers`, `products`, `orders`, `order_items`,
`payments`. Use an upsert or truncate-and-reload strategy so rerunning the script does not
create duplicates.

---

## Data validation checklist

Complete these checks before answering the business questions:

1. Confirm the expected counts: 80 orders, 199 order items, 12 distinct customers,
   10 distinct products, and 80 payments.
2. Check primary keys for nulls and duplicates.
3. Confirm every foreign key has a matching parent row.
4. Check that each product ID always maps to the same name, category, and catalogue price.
5. Recalculate each `line_total` as
   `quantity × unit_price × (1 − discount_pct / 100)`.
6. Confirm each order's `subtotal` equals the sum of its item totals.
7. Confirm `order_total = subtotal + delivery_fee`.
8. Compare payment amount with order total and explain how cancelled, pending, and
   refunded records should be treated.
9. Validate that dates fall between 5 January and 28 July 2026 and that quantities,
   prices, discounts, fees, and delivery days are within sensible ranges.
10. Record every transformation and failed check; never silently delete a row.

**Sales rule:** unless a question says otherwise, use `status = 'Completed'` and
`payment_status = 'Paid'` for realized sales. Treat cancelled, refunded, and pending
orders separately rather than counting them as revenue.

---

## The 10 analysis questions

Answer each question in SQL, then reproduce the important totals in Python or Power BI.

### Q1 — JSON profiling and reconciliation

Produce a validation report using the checklist above. Include expected and actual row
counts, duplicate IDs, orphan records, and the number and value of any reconciliation
differences. Explain why order-level totals must not be summed after joining directly to
`order_items` without first controlling the table grain.

### Q2 — Monthly sales performance

For completed and paid orders, calculate monthly order count, unique customers, item
quantity, subtotal, delivery fees, realized sales, average order value, and month-over-
month sales growth. Identify the strongest month, but note that January and July cover
only the dates present in the file and that the dataset contains just seven months.

### Q3 — Product and category performance

Rank products by realized line-item sales and units sold. Add each product's percentage
of category sales and its rank within the category. Compare catalogue price with the
transaction price and identify categories that drive high sales through price versus
volume.

### Q4 — Discount effectiveness

Group completed line items into useful discount bands and compare units, sales, and
average line value. Calculate discount value as the pre-discount value minus
`line_total`. Which products receive the most discount in KES, and is a higher discount
associated with larger quantities in this small dataset? Do not claim causation.

### Q5 — Customer and segment value

For each customer, calculate completed orders, realized sales, average order value,
first order date, last order date, and days since last order relative to 28 July 2026.
Rank customers within their segment and compare Consumer, Corporate, and Small Business
performance.

### Q6 — Repeat purchasing and simple RFM

Calculate Recency, Frequency, and Monetary value for every customer using completed and
paid orders. Create clearly documented score bands that work with only 12 customers.
Identify repeat customers and compare their average order value with one-time customers.

### Q7 — Channel and location performance

Compare Mobile App, Website, and Physical Store by attempted orders, completion rate,
realized sales, average order value, and discount value. Repeat the analysis for customer
city and shipping city. Count orders where the two cities differ and test whether those
orders have different delivery fees or delivery times.

### Q8 — Payment and order status

Build a matrix of order status by payment status and payment method. Calculate payment
success, refund, and pending rates by method and channel. Quantify the value tied up in
pending orders and the value associated with refunded orders; do not label either as
realized revenue.

### Q9 — Delivery operations

For completed orders, calculate average delivery fee and average delivery days by
shipping city, channel, and order-value band. Compare free and paid delivery orders.
Identify unusually slow orders using a documented threshold, and state whether the data
records promised or actual delivery days because the source does not explicitly say.

### Q10 — Market basket analysis

Create distinct unordered product pairs from items within the same order, avoiding self-
pairs and mirrored duplicates. Rank pairs by number of orders together and calculate
support. Repeat at category level. Recommend two cross-sell bundles while acknowledging
that 80 orders are not enough to establish stable purchasing patterns.

---

## Power BI dashboard requirements

Build the same five-table model in Power BI and mark the relationships as one-to-many in
the direction shown above. Create measures rather than calculated columns for totals that
must respond to filters.

### Page 1 — Executive overview

- Cards: realized sales, completed orders, units sold, average order value, and completion rate
- Monthly sales and order trend
- Sales by category and channel
- Top five products and customers
- Slicers for date, city, segment, channel, status, and payment method

### Page 2 — Customer and product analysis

- Customer/segment matrix with sales, frequency, and average order value
- Product sales and quantity ranking
- Discount-band comparison
- Product-pair or category-pair cross-sell visual

### Page 3 — Payments and delivery

- Payment-status and order-status matrix
- Payment outcomes by method and channel
- Pending and refunded value cards
- Delivery days and fees by shipping city
- Table of unusually slow orders

Ensure every visual states whether it uses all attempted orders or only completed and paid
orders. Format financial measures as KES and add a short business interpretation to each
dashboard page.

---

## Suggested deliverables

1. `01_json_profiling.ipynb` — inspect, validate, and normalize the JSON
2. `load_retail_data.py` — repeatable PostgreSQL loader
3. `schema.sql` — table definitions, keys, checks, and indexes
4. `queries.sql` — one commented, runnable solution per analysis question
5. `kenya_retail_sales.pbix` — three-page Power BI report
6. `README.md` — 6–10 findings, assumptions, limitations, and recommendations

Do not commit database credentials, generated database files, or an exported copy of the
source data.

## Marking guide

| Criterion | Weight |
|---|---:|
| Normalization and referential integrity | 25% |
| Validation and reconciliation | 20% |
| SQL correctness and appropriate table grain | 25% |
| Power BI model, measures, and visual clarity | 20% |
| Reproducibility and business communication | 10% |

## Stretch goals

- Add indexes on every foreign key and compare query plans with `EXPLAIN ANALYZE`.
- Build a star schema with date, customer, product, and channel dimensions.
- Use dbt staging models and tests for uniqueness, relationships, and accepted values.
- Create an incremental loader that records the source file name and ingestion timestamp.
- Publish a one-page data-quality scorecard alongside the business dashboard.

## Data provenance

The JSON is a synthetic practice dataset. Treat the committed file as the reproducible
source and preserve it unchanged.
