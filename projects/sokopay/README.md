# SokoPay Kenya — Data Analytics Project Brief

**Dataset:** [`kenya_transactions.csv`](./kenya_transactions.csv) · 15,070 rows · 25 columns · 1 Jan 2025 → 30 Jun 2026

You are an analyst at **SokoPay**, a Kenyan digital payments and marketplace platform
operating across 14 counties. Customers pay merchants through the mobile app, USSD, web,
or a physical agent outlet. Leadership wants to understand growth, reliability, and
customer behaviour before the next funding round.

The data is synthetic but behaves like production data: it has seasonality, payday
spikes, hourly peaks, customer churn, a long tail of merchants — and **real data quality
problems that were left in on purpose.** Do not assume it is clean.

---

## Data dictionary

| Column | Type | Notes |
|---|---|---|
| `transaction_id` | text | Intended to be unique — verify this |
| `transaction_ts` | timestamp | `YYYY-MM-DD HH:MM:SS`, the event time |
| `customer_id` | text | Links transactions to a customer |
| `customer_name` | text | |
| `gender` | text | Female / Male |
| `age` | integer | Has nulls and impossible values |
| `signup_date` | date | Date the customer joined the platform |
| `county` | text | 14 counties; casing and whitespace are inconsistent |
| `town` | text | Sub-location within the county |
| `merchant_id` | text | 120 merchants |
| `merchant_name` | text | Names are **not** unique — always join on `merchant_id` |
| `category` | text | 10 product categories |
| `product` | text | |
| `quantity` | integer | |
| `unit_price_kes` | numeric | Price per unit in KES |
| `discount_pct` | integer | 0–25 |
| `amount_kes` | numeric | Charged amount — should reconcile to qty × price × (1 − discount) |
| `delivery_fee_kes` | numeric | 0 for digital categories |
| `channel` | text | Mobile App / USSD / Web / Agent Outlet |
| `payment_method` | text | M-Pesa / Airtel Money / Card / Cash / Bank Transfer |
| `device_os` | text | Android / iOS / Feature Phone / Web Browser |
| `status` | text | Completed / Pending / Failed / Refunded / Cancelled |
| `rating` | integer | 1–5, only on some completed orders (missing ≠ zero) |
| `session_id` | text | Platform-assigned session — one of the questions asks you to challenge it |
| `delivery_days` | integer | Days to delivery, only where a delivery fee applied |

**Revenue rule for every question below:** unless stated otherwise, revenue counts
`amount_kes + delivery_fee_kes` for `status = 'Completed'` only.

---

## Setup

**Python**
```python
import pandas as pd
df = pd.read_csv("kenya_transactions.csv", parse_dates=["transaction_ts", "signup_date"])
```

**PostgreSQL**
```sql
CREATE TABLE transactions (
    transaction_id    TEXT,
    transaction_ts    TIMESTAMP,
    customer_id       TEXT,
    customer_name     TEXT,
    gender            TEXT,
    age               INTEGER,
    signup_date       DATE,
    county            TEXT,
    town              TEXT,
    merchant_id       TEXT,
    merchant_name     TEXT,
    category          TEXT,
    product           TEXT,
    quantity          INTEGER,
    unit_price_kes    NUMERIC,
    discount_pct      INTEGER,
    amount_kes        NUMERIC,
    delivery_fee_kes  NUMERIC,
    channel           TEXT,
    payment_method    TEXT,
    device_os         TEXT,
    status            TEXT,
    rating            INTEGER,
    session_id        TEXT,
    delivery_days     INTEGER
);

\copy transactions FROM 'kenya_transactions.csv' WITH (FORMAT csv, HEADER true, NULL '');
```

---

## The 10 questions

Answer each one **twice** — once in pandas, once in SQL — and confirm the two agree.
Where they disagree, the reason is usually more interesting than the number.

### Q1 — Data quality audit (do this first)

Produce a data quality report covering: exact duplicate rows, duplicated
`transaction_id` values that are *not* full duplicates, near-duplicate transactions
(same customer and merchant within 60 seconds — likely a double-tap), inconsistent
`county` values caused by casing and whitespace, missing values per column, impossible
values in `age` and `quantity`, and rows where `amount_kes` does not reconcile to
`quantity × unit_price_kes × (1 − discount_pct/100)` within 1 KES.

Then write a **documented cleaning function** and save `transactions_clean.csv`. Every
row you drop or change must be counted and justified. All later questions run on the
clean data.

> *Python:* `duplicated`, `str.strip().str.title()`, `np.isclose`, boolean masks
> *SQL:* `ROW_NUMBER() OVER (PARTITION BY ...)`, `LAG` with `INTERVAL`, `TRIM`/`INITCAP`, `ABS(a - b) > 1`

### Q2 — Monthly growth with a rolling trend

Build a monthly revenue series and add: month-over-month growth %, a 3-month centred
rolling average, and each month's share of the running cumulative total. Identify the
single strongest month and quantify how much of the year-on-year change is explained by
December alone. Finally, split the trend into transaction **volume** vs average **basket
size** — is SokoPay growing because more people buy, or because they spend more?

> *Python:* `resample("MS")`, `rolling(3, center=True)`, `pct_change`, `cumsum`
> *SQL:* `DATE_TRUNC`, `LAG(...) OVER (ORDER BY month)`, `AVG(...) OVER (ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)`

### Q3 — When is SokoPay busiest?

Build a 7 × 24 matrix of transaction volume by day-of-week and hour, and a second one for
average value. Find the top 5 hour-blocks by revenue. Then test the payday hypothesis:
are the last 3 and first 3 days of the month materially busier than mid-month? Report the
lift as a percentage and state your assumptions. Repeat the analysis split by county —
does Nairobi peak at the same time as Kisumu?

> *Python:* `dt.dayofweek`, `dt.hour`, `pivot_table`, a seaborn heatmap
> *SQL:* `EXTRACT(DOW ...)`, `EXTRACT(HOUR ...)`, `FILTER (WHERE ...)`, conditional aggregation

### Q4 — Cohort retention

Group customers into monthly cohorts by `signup_date`. For each cohort, compute the
percentage still transacting in month 0, 1, 2, … 12 after signup. Present it as a
triangular retention table and identify which cohort retains best. Then compute
**revenue retention** (KES per original cohort member per month) and explain why it can
rise while user retention falls.

> *Python:* `to_period("M")`, cohort index arithmetic, `pivot_table`, `div(axis=0)`
> *SQL:* `DATE_TRUNC` on signup, `AGE()` / month arithmetic, `COUNT(DISTINCT ...)`, a self-join to the cohort size table

### Q5 — RFM segmentation

For each customer compute Recency (days since last transaction relative to 30 Jun 2026),
Frequency, and Monetary value. Score each 1–5 using quintiles and assign segments:
Champions, Loyal, Potential Loyalist, At Risk, Hibernating, Lost. Report how many
customers and how much revenue sit in each segment, and name the segment that is
**small in headcount but large in revenue** — that is who the retention team should
call first.

> *Python:* `groupby.agg`, `pd.qcut`, `np.select`
> *SQL:* `NTILE(5) OVER (ORDER BY ...)`, `CASE WHEN`, CTEs

### Q6 — Sessionization (gaps and islands)

Ignore the `session_id` column. Rebuild sessions yourself: a customer's transactions
belong to the same session if consecutive events are less than 30 minutes apart.
Compute sessions per customer, transactions per session, and session revenue. Then
compare your sessions against the platform's `session_id` — how badly does the platform
over-count? Quantify the disagreement.

> *Python:* sort, `groupby.diff()`, `gt(pd.Timedelta("30min")).cumsum()`
> *SQL:* `LAG(transaction_ts) OVER (PARTITION BY customer_id ORDER BY transaction_ts)`, `SUM(new_session_flag) OVER (...)`

### Q7 — Merchant league table and concentration

Rank merchants by revenue **within each county**, keeping the top 3 per county. Add each
merchant's share of its county's revenue and a dense rank nationally. Then measure
concentration: what percentage of total revenue comes from the top 10% of merchants?
Plot the Lorenz curve and compute the Gini coefficient. Is SokoPay dangerously dependent
on a handful of merchants?

> *Python:* `groupby(...).rank(method="dense")`, `nlargest`, `transform("sum")`, `cumsum` for the Lorenz curve
> *SQL:* `RANK()` / `DENSE_RANK()` / `PERCENT_RANK()` in a window, filtered in an outer query, `SUM(...) OVER ()` for the share

### Q8 — Why do transactions fail?

Compute the failure rate (`status = 'Failed'`) by channel, by payment method, and by the
two crossed. Test whether failure rate depends on the hour of day. Run a chi-square test
of independence between channel and outcome, report the p-value, and state the business
recommendation in one sentence. Then estimate the **revenue at risk**: how many KES of
attempted transactions failed in the last 6 months?

> *Python:* `crosstab`, `scipy.stats.chi2_contingency`
> *SQL:* conditional aggregation with `COUNT(*) FILTER (WHERE status = 'Failed')::NUMERIC / COUNT(*)`, `GROUPING SETS` or `ROLLUP`

### Q9 — Category affinity (market basket)

Using only customers with 3 or more transactions, find which pairs of categories are
bought by the same customer more often than chance would predict. Compute support,
confidence, and lift for the top 15 category pairs. Then answer the merchandising
question: if a customer's first-ever purchase is in Airtime & Data, which category are
they most likely to buy next?

> *Python:* self-merge on `customer_id`, `itertools.combinations`, filter `A < B` to avoid mirrored pairs
> *SQL:* self-join `ON a.customer_id = b.customer_id AND a.category < b.category`, plus a first-purchase CTE using `ROW_NUMBER()`

### Q10 — Churn features and a baseline model

Define churn as: no transaction in the 60 days before 30 Jun 2026, for customers whose
first transaction was at least 90 days earlier. Engineer a customer-level feature table —
tenure, transaction count, total and average spend, average inter-purchase interval and
its standard deviation, dominant channel and county, failure rate experienced, average
rating given, spend in the last 30 days vs the previous 30 (a trend ratio).

Build the feature table **in SQL** as a single query, export it, then train logistic
regression and a random forest in scikit-learn. Report precision, recall, ROC-AUC and a
confusion matrix, and rank feature importance. Which behaviour predicts churn earliest?

> *Python:* `train_test_split` with `stratify`, `ClassifierMixin`, `classification_report`
> *SQL:* multiple CTEs, `MAX`/`MIN` on timestamps, `LAG` for inter-purchase gaps, `AVG` of intervals, `FILTER` clauses for windowed spend

---

## Deliverables

1. `01_cleaning.ipynb` — Q1, plus `transactions_clean.csv`
2. `02_analysis.ipynb` — Q2–Q9 in pandas, with charts
3. `queries.sql` — one commented, runnable query per question
4. `03_modelling.ipynb` — Q10
5. `README.md` — 8–10 findings written for a business reader, no code, no jargon

## Marking guide

| Criterion | Weight |
|---|---|
| Correctness — Python and SQL answers reconcile | 30% |
| Data quality handling — decisions documented, not silently dropped | 20% |
| SQL sophistication — window functions and CTEs over nested subqueries | 20% |
| Communication — charts labelled, findings stated as business insight | 20% |
| Reproducibility — runs top to bottom on a clean kernel | 10% |

## Stretch goals

- Load the CSV into PostgreSQL with an idempotent Python ingestion script
- Model it as a star schema (fact + customer, merchant, date dimensions) and rewrite Q7 against it
- Orchestrate cleaning → load → aggregate as an Airflow DAG
- Build the county and channel views as dbt models with tests on uniqueness and not-null
- Serve the Q10 churn model behind a FastAPI endpoint
