# Kenya Agentic Payments — Student Analytics Project Brief

**Dataset:** [`kenya_agentic_payments.csv`](./kenya_agentic_payments.csv) · 8,002 rows · 25 columns · 1 Jan 2026 → 31 Jul 2026

You are a data analyst for **HakikishaPay**, a fictional Kenyan fintech building payment rails for AI agents that can pay merchants, contractors, consumers, and other agents. The leadership team wants to understand whether the product is safe, fast, and useful enough for Kenyan SMEs before expanding from Nairobi, Kiambu, Mombasa, and Nakuru into more counties.

The data is fully synthetic. It is designed to feel relatable in Kenya: counties and towns are Kenyan, rails include M-Pesa, Airtel Money, PesaLink, bank EFT, and stablecoin settlement, and use cases include property maintenance, market restocking, school fees, clinic supplies, logistics, construction, and agritech purchases.

> **Important:** intentional data quality issues are included. Do not assume the file is clean.

---

## Scenario

AI agents can already request quotes, schedule jobs, reconcile invoices, and negotiate tasks. The difficult step is moving money safely without a human manually approving every payment. HakikishaPay gives each organization controlled wallets, policy rules, counterparty checks, and an authorization layer for three payment flows:

- **A2B:** agent-to-business payments, such as paying a contractor, school, clinic, or merchant.
- **A2A:** agent-to-agent payments, such as paying a specialist logistics or data-labelling agent.
- **A2C:** agent-to-consumer disbursements, such as refunds or small payouts.

Your job is to produce a clean analysis that answers: **which payment flows are growing, where are the risks, which rails are fast and affordable, and when should a human stay in the loop?**

---

## Data dictionary

| Column | Type | Notes |
|---|---|---|
| `payment_id` | text | Intended unique payment reference; verify duplicates. |
| `requested_at` | timestamp | Time the agent requested authorization. |
| `organization_id` | text | Business using HakikishaPay. |
| `wallet_id` | text | Controlled wallet used for the payment. |
| `agent_id` | text | Agent that initiated the payment. |
| `agent_type` | text | Agent role, such as procurement, property management, logistics, marketplace, or finance ops. |
| `flow_type` | text | A2B, A2A, or A2C. |
| `use_case` | text | Business reason for payment. |
| `counterparty_id` | text | Receiving party identifier. |
| `counterparty_type` | text | Merchant, contractor, consumer, agent service, school, Sacco, or clinic. |
| `county` | text | Kenyan county; has intentional casing/whitespace issues. |
| `town` | text | Town or neighbourhood. |
| `rail` | text | Payment rail used. |
| `amount_kes` | numeric | Requested payment amount in Kenyan shillings. |
| `fee_kes` | numeric | Fee charged for authorization and settlement. |
| `status` | text | Completed, Failed, Reversed, Needs Human Approval, or Flagged. |
| `human_approval_required` | boolean | Whether policy required a human review before release. |
| `risk_score` | numeric | Model/rules risk score from 0 to 1. |
| `risk_reason` | text | Main reason for risk decision; `none` for ordinary completed payments. |
| `authorization_latency_ms` | integer | Time from agent request to authorization decision. |
| `policy_version` | integer | Version of the wallet/risk policy applied. |
| `wallet_balance_before_kes` | numeric | Wallet balance before the payment decision. |
| `wallet_balance_after_kes` | numeric | Wallet balance after completed or held payment. |
| `invoice_id` | text | Optional invoice reference. |
| `decision_model` | text | Model or rules engine used for the decision. |

**Revenue rule:** unless a question says otherwise, count revenue as `fee_kes` for `status = 'Completed'` payments only.

---

## Getting started

### Python

```python
import pandas as pd

payments = pd.read_csv(
    "kenya_agentic_payments.csv",
    parse_dates=["requested_at"]
)
print(payments.shape)
payments.head()
```

### PostgreSQL

```sql
CREATE TABLE agentic_payments (
    payment_id                    TEXT,
    requested_at                  TIMESTAMP,
    organization_id               TEXT,
    wallet_id                     TEXT,
    agent_id                      TEXT,
    agent_type                    TEXT,
    flow_type                     TEXT,
    use_case                      TEXT,
    counterparty_id               TEXT,
    counterparty_type             TEXT,
    county                        TEXT,
    town                          TEXT,
    rail                          TEXT,
    amount_kes                    NUMERIC,
    fee_kes                       NUMERIC,
    status                        TEXT,
    human_approval_required       BOOLEAN,
    risk_score                    NUMERIC,
    risk_reason                   TEXT,
    authorization_latency_ms      INTEGER,
    policy_version                INTEGER,
    wallet_balance_before_kes     NUMERIC,
    wallet_balance_after_kes      NUMERIC,
    invoice_id                    TEXT,
    decision_model                TEXT
);

\copy agentic_payments FROM 'kenya_agentic_payments.csv' WITH (FORMAT csv, HEADER true, NULL '');
```

---

## The 10 student tasks

Answer each question in **Python and SQL**, then compare the results.

### Q1 — Data quality and cleaning plan

Create a data quality report covering row count, duplicate rows, duplicated `payment_id` values, missing values, inconsistent `county` values, negative or zero `amount_kes`, non-positive `authorization_latency_ms`, risk scores outside 0–1, and balance rows where a completed payment does not approximately equal `wallet_balance_before_kes - amount_kes - fee_kes`.

Deliver a documented cleaning function or SQL cleaning view and explain every row dropped or changed.

### Q2 — Monthly growth and fee revenue

For completed payments, calculate monthly payment value, fee revenue, payment count, and month-over-month fee revenue growth. Which month grew fastest, and was the growth driven more by transaction count or average payment size?

### Q3 — Flow mix: A2B vs A2A vs A2C

Compare payment count, total value, median amount, average fee rate, failure/flag rate, and human approval rate by `flow_type`. Which flow looks most ready for autonomous scale, and which needs stronger controls?

### Q4 — Rail performance scorecard

Build a scorecard by `rail` showing completed payment value, average fee, average effective fee rate (`fee_kes / amount_kes`), p50 and p95 authorization latency, failure/reversal/flag rate, and human approval rate. Recommend the best rail for high-volume SME payments in Kenya.

### Q5 — Counterparty trust and KYB risk

Rank counterparties by completed value and by risk events. Identify counterparties with high value but frequent `kyb_pending`, `new_counterparty`, or `mismatched_invoice` reasons. Propose a simple counterparty trust tiering rule.

### Q6 — Human-in-the-loop policy analysis

Compare payments where `human_approval_required = true` vs false. Measure average amount, risk score, completion rate, latency, and fee revenue. Estimate how many manual reviews could be avoided if payments below KES 10,000 and risk score below 0.25 were auto-approved.

### Q7 — County expansion analysis

Normalize county names, then compare adoption by county: organizations served, agents active, completed value, approval rate, and top use case. Which three counties should HakikishaPay prioritize next, and why?

### Q8 — Wallet controls and exposure

For each `wallet_id`, compute total completed value, largest single payment, number of unique counterparties, human approval rate, and the lowest observed post-payment balance. Flag wallets where the largest single payment exceeds 50% of the observed starting balance or where the balance appears inconsistent.

### Q9 — Agent behavior and anomaly detection

For each `agent_id`, calculate payment frequency, median amount, maximum amount, risk event rate, and number of counties touched. Flag agents with high velocity, unusually high maximum amounts, or broad geographic spread. Explain whether each flag is necessarily fraud or could be normal business behaviour.

### Q10 — Executive dashboard

Create a one-page dashboard for a Kenyan fintech leadership team. Include at least: monthly completed value, rail performance, flow mix, county map or county bar chart, risk reasons, human approval funnel, and top counterparties. Write five executive insights and three recommended actions.

---

## Suggested deliverables

1. A notebook with Python cleaning and analysis.
2. A SQL script with reproducible queries or views for all 10 tasks.
3. A cleaned CSV saved outside this source folder, with a short cleaning log.
4. A dashboard screenshot or exported PDF.
5. A one-page executive memo written for a fintech founder, not just a technical audience.

---

## Data provenance

This dataset is synthetic and generated for practice. It does not contain real organizations, people, wallets, invoices, or payment records.
