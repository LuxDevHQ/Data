# Twiga Trails Safaris — Power BI Workshop Kit

End-to-end Power BI project for the **LuxDevHQ Data Analytics cohort**, led by **Caleb Kilemba**.
Learners take eight messy source files from a fictional Nairobi safari operator all the way to a
secured, scheduled-refresh report in Power BI Service.

## What's in the folder

| Path | What it is |
|---|---|
| `Workshop_Handbook.html` | The full handbook: brief, agenda, 9 modules, M + DAX code, checkpoints, rubric, answer key. Open in any browser; prints cleanly. |
| `data/Bookings/` | Booking files for 2023–2025 (fact table, loaded with the Folder connector) |
| `data/_later/Bookings_2026_H1.csv` | Move this into `data/Bookings/` during Module 8 to show a refresh picking up a new file |
| `data/Customers.xlsx` | Customer master: title rows and 46 country spellings to clean |
| `data/*.csv` | Packages, Parks, Agents, Regions (RLS), Reviews, Targets |
| `answer_key.json` | Every checkpoint figure, calculated from the cleaned data |
| `generate_data.py` | Rebuilds the dataset and answer key (fixed seed, so output is identical every run) |

## Six data traps (spoilers for facilitators)

1. 37 duplicate bookings in `Bookings_2024.csv`
2. Status values with inconsistent casing, trailing spaces, and "Canceled"
3. Blank `DiscountPct` (means 0)
4. Blank `AgentID` for 2023 website bookings (means `AG00`)
5. Two title rows above the header in `Customers.xlsx`
6. 17 countries spelled 46 different ways

## Facilitator prep

- Replace the four `ManagerEmail` values in `data/Regions.csv` with real learner work/school emails so the dynamic RLS demo works.
- Create the cohort workspace in Power BI Service and confirm licensing before the day.
- Zip the folder **without** `answer_key.json` for learners if you want them to rely only on the checkpoints in the handbook.

## Regenerate

```bash
python3 generate_data.py
```

Requires Python 3 with `openpyxl`.

All companies, people and figures are fictional.
