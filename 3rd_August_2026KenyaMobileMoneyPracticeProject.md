# Kenya Mobile Money — Python and SQL Practice Project

## Project Overview

This project gives you a **synthetic Kenyan mobile-money transactions dataset**
(M-Pesa / Airtel Money / T-Kash / Equitel style) so you can practise real
data-science and analytics skills with **Python (pandas)** and **SQL**.

All data is **randomly generated and fully synthetic** — no real people, phone
numbers, or accounts. The dataset is designed to be messy and realistic enough
that the questions below require *advanced* techniques: window functions,
cohort/retention analysis, time-series resampling, RFM segmentation, and more.

**Dataset:** [`kenya_mobile_money_transactions.csv`](./kenya_mobile_money_transactions.csv)
— 6,000 transactions across 800 customers, spanning **1 Jan 2024 → 31 Dec 2024**.

---

## Dataset Dictionary

| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | Unique transaction reference (e.g. `TXN0000142`) |
| `transaction_timestamp` | datetime | Date and time of the transaction (`YYYY-MM-DD HH:MM:SS`) — **the time column** |
| `customer_id` | string | Unique customer reference (e.g. `CUST00093`) |
| `customer_name` | string | Customer full name (Kenyan names) |
| `gender` | string | `Male` / `Female` |
| `age` | int | Customer age in years (18–72) |
| `county` | string | Kenyan county of the customer |
| `phone_number` | string | Masked/synthetic Safaricom/Airtel-style number |
| `channel` | string | `M-Pesa`, `Airtel Money`, `T-Kash`, `Equitel` |
| `transaction_type` | string | `Send Money`, `Buy Goods (Till)`, `Pay Bill`, `Withdraw Cash`, `Deposit Cash`, `Airtime Purchase`, `Reversal` |
| `merchant_category` | string | Sector for Till/Paybill (e.g. `Supermarket`, `KPLC`, `School Fees`); `N/A` otherwise |
| `device_type` | string | `Android`, `Feature Phone`, `iOS` |
| `amount_kes` | float | Transaction amount in Kenyan Shillings |
| `transaction_fee_kes` | float | Fee charged in KES |
| `balance_after_kes` | float | Wallet balance after the transaction |
| `status` | string | `Completed`, `Failed`, `Reversed` |

---

## Getting Started

**Python**

```python
import pandas as pd

df = pd.read_csv("kenya_mobile_money_transactions.csv",
                 parse_dates=["transaction_timestamp"])
print(df.shape)
df.head()
```

**SQL (PostgreSQL example)**

```sql
CREATE TABLE transactions (
    transaction_id         VARCHAR(20) PRIMARY KEY,
    transaction_timestamp  TIMESTAMP,
    customer_id            VARCHAR(20),
    customer_name          VARCHAR(100),
    gender                 VARCHAR(10),
    age                    INT,
    county                 VARCHAR(50),
    phone_number           VARCHAR(20),
    channel                VARCHAR(30),
    transaction_type       VARCHAR(30),
    merchant_category      VARCHAR(50),
    device_type            VARCHAR(20),
    amount_kes             NUMERIC(12,2),
    transaction_fee_kes    NUMERIC(12,2),
    balance_after_kes      NUMERIC(12,2),
    status                 VARCHAR(20)
);
-- Then import the CSV (e.g. \copy transactions FROM 'kenya_mobile_money_transactions.csv' CSV HEADER;)
```

---

## The 10 Advanced Questions

Solve **each question twice** — once in Python (pandas) and once in SQL. Compare
your answers. The point is to build fluency in *window functions, time-series
grouping, and segmentation*, not just simple aggregation.

> Note: analyse only `status = 'Completed'` transactions unless a question says
> otherwise.

### 1. Monthly revenue trend and month-over-month growth
Compute total **fee revenue** (`transaction_fee_kes`) per calendar month, then
add a column showing the **month-over-month % change**. Which month grew fastest?
*(Skills: time bucketing, `LAG()` / `.pct_change()`.)*

### 2. Peak transaction hours (heatmap-ready)
Build a **day-of-week × hour-of-day** matrix of transaction counts. Identify the
single busiest hour block. *(Skills: extracting hour & weekday from a timestamp,
pivoting.)*

### 3. Top customers by value, ranked within their county
For each county, rank customers by **total amount transacted** and return the
**top 3 per county**. *(Skills: `RANK()` / `ROW_NUMBER()` partitioned by county,
or `groupby().rank()`.)*

### 4. 7-day rolling transaction volume
Create a daily transaction-count series, then compute the **7-day rolling
average** of daily volume. On how many days did volume exceed 1.5× its rolling
average? *(Skills: resampling to daily, rolling windows.)*

### 5. Customer RFM segmentation
For every customer compute **Recency** (days since last transaction, relative to
the dataset's max date), **Frequency** (number of transactions), and **Monetary**
(total amount). Score each into quintiles (1–5) and label the top segment as
"Champions". *(Skills: multi-metric aggregation, quantile bucketing, `NTILE()`.)*

### 6. Failure/reversal rate by channel and transaction type
Using **all** statuses, compute the percentage of transactions that are
`Failed` or `Reversed`, broken down by `channel` × `transaction_type`. Which
combination is least reliable? *(Skills: conditional aggregation, ratio over
groups.)*

### 7. Fee efficiency by transaction band
Bucket transactions into amount bands (`0–500`, `501–1,000`, `1,001–5,000`,
`5,001–20,000`, `20,000+`) and compute the **average effective fee rate**
(`fee / amount`) per band. Does the fee structure favour large or small
transactions? *(Skills: `CASE` / `pd.cut`, ratio metrics.)*

### 8. Customer inter-transaction gap
For each customer, order their transactions by time and compute the **average
number of days between consecutive transactions**. List the 10 most active
(smallest average gap) customers. *(Skills: `LAG()` over a partition ordered by
time, or `groupby().diff()`.)*

### 9. Monthly new vs returning customers (cohorts)
Assign each customer to the **month of their first transaction** (their cohort).
For each subsequent month, count how many customers are transacting for the
first time ("new") vs already seen ("returning"). *(Skills: first-seen per
group, cohort assignment, self-comparison across periods.)*

### 10. County revenue concentration (Pareto / 80-20)
Rank counties by total transaction value and compute the **cumulative % of total
value**. How few counties account for 80% of all money moved? *(Skills: ordered
cumulative sums, window `SUM() OVER (ORDER BY ...)`, Pareto analysis.)*

---

## Suggested Deliverables

1. A Jupyter notebook (`.ipynb`) with a pandas solution for each question.
2. A `.sql` file with one query per question.
3. A short write-up (3–5 bullet points) of the **business insights** you found —
   e.g. which counties to prioritise, which channel is least reliable, when the
   platform is busiest.
4. **Bonus:** turn Questions 1, 2, and 10 into charts (Matplotlib/Seaborn or
   Power BI).

---

## How the Data Was Generated

The dataset is produced by
[`scripts/generate_kenya_mobile_money.py`](./scripts/generate_kenya_mobile_money.py),
seeded (`random.seed(42)`) for reproducibility. Re-run it to regenerate an
identical file, or change the seed / `N_ROWS` to produce a different sample.
