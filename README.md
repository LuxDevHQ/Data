# Data Practice Hub

A collection of beginner-friendly datasets and guided analytics projects for learning **Excel, SQL, Python, and Power BI**. All material is grouped by purpose so you can choose a guided project or explore a standalone dataset without searching through unrelated files.

## Start here

1. **Choose your level.** Start with a standalone dataset if you are new to analysis; choose a guided project when you are comfortable filtering and grouping data.
2. **Read before opening the data.** Each project has its own README with a data dictionary, setup instructions, questions, and expected deliverables.
3. **Work in your own folder.** Create a notebook, SQL script, or dashboard outside the source-data folders so the original datasets stay unchanged.
4. **Validate your work.** Check row counts, missing values, duplicates, data types, and totals before drawing conclusions.
5. **Explain the result.** Record the method, assumptions, and a short business interpretation for every answer.

## Guided projects

| Project | Level | Data | What you will practise |
|---|---|---|---|
| [Kenya retail sales](projects/kenya-retail-sales/) | Beginner–intermediate | Nested JSON, 80 orders / 199 items | JSON normalization, relational modelling, SQL, Power BI |
| [Kenya mobile money](projects/kenya-mobile-money/) | Intermediate | CSV, 6,000 transactions | pandas, SQL windows, time series, RFM, cohorts |
| [SokoPay Kenya](projects/sokopay/) | Advanced | CSV, 15,070 transactions | data cleaning, retention, sessionization, statistics, modelling |
| [Hospital operations](projects/hospital-operations/) | Beginner–intermediate | Excel workbook with related sheets | PostgreSQL import, joins, operational KPIs, Power BI |

### Recommended learning order

- **New analyst:** Hospital operations → Kenya retail sales → Kenya mobile money → SokoPay.
- **SQL learner:** Follow the [PostgreSQL guide](docs/postgresql-guide.md), then solve a project's questions in SQL.
- **Python learner:** Start with Kenya mobile money and compare each pandas result with SQL.
- **Portfolio builder:** Complete SokoPay and publish a cleaned notebook, reproducible SQL, labelled charts, and an executive summary.

## Standalone datasets

These files do not have a required sequence. Profile one, decide on a question, clean a copy, and document your findings.

### CSV

| File | Topic | Suggested first exercise |
|---|---|---|
| [`Global_Superstore2.csv`](datasets/csv/Global_Superstore2.csv) | International retail orders | Compare sales and profit by region and category. |
| [`data_engineer_salaries.csv`](datasets/csv/data_engineer_salaries.csv) | Data-engineering salary ranges | Compare average salary by level and country. |

### Excel

| File | Topic | Suggested first exercise |
|---|---|---|
| [`excel_sales_project.xlsx`](datasets/excel/excel_sales_project.xlsx) | Sales and customers | Build a monthly sales summary and check returns. |
| [`supermarket_transactions.csv.xlsx`](datasets/excel/supermarket_transactions.csv.xlsx) | Supermarket transactions | Profile and repair inconsistent or shifted fields before analysis. |

### JSON

The [`datasets/json`](datasets/json/) directory contains small practice files about users, students, cars, and Kenyan data. Use these to practise reading nested data, normalizing records into tables, and checking schemas. Inspect the structure first: similarly named files may have different fields and should not be combined without validation.

## A simple study workflow

```text
1. Define one question
2. Inspect the schema and data types
3. Audit missing, invalid, and duplicate values
4. Clean a copy (never overwrite the source)
5. Analyse in small, testable steps
6. Cross-check important totals
7. Visualize only what helps answer the question
8. Write the finding, assumptions, and limitations
```

For SQL setup examples, table definitions, import guidance, and 30 practice questions, see the [PostgreSQL guide](docs/postgresql-guide.md). Paths in that guide are relative to the repository root unless noted otherwise.

## Repository map

```text
.
├── README.md                       # orientation and learning path
├── docs/
│   └── postgresql-guide.md         # SQL setup and exercises
├── datasets/
│   ├── csv/                        # standalone CSV datasets
│   ├── excel/                      # standalone Excel workbooks
│   └── json/                       # standalone JSON datasets
└── projects/
    ├── hospital-operations/        # brief and workbook
    ├── kenya-retail-sales/         # nested-JSON retail project brief
    ├── kenya-mobile-money/         # brief and CSV
    └── sokopay/                    # brief and CSV
```

## Data-use notes

- Treat names, emails, and phone-like values as practice data; do not use them to contact or identify anyone.
- Project datasets described as synthetic should still be handled responsibly in screenshots and published work.
- Large source files are intentionally kept out of generated outputs. Avoid committing database files, exported dashboards, or duplicate cleaned datasets unless they are a required deliverable.
