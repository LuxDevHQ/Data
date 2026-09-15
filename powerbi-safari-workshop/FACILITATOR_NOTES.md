# Twiga Trails Safaris — Facilitator Notes

These notes are for Caleb Kilemba and other facilitators delivering the Power BI workshop to the LuxDevHQ Data Analytics cohort. Give learners the [student guide](README.md), not this spoiler file, while they profile the sources.

## Intentional data-quality traps

1. `data/Bookings/Bookings_2024.csv` contains 37 duplicate bookings.
2. `Status` contains inconsistent casing, trailing spaces, and the US spelling `Canceled`.
3. Some `DiscountPct` values are blank. Blank means 0.
4. `AgentID` is blank for 1,100 website bookings in 2023. Blank means `AG00`.
5. `data/Customers.xlsx` has a title row and a blank row above the real header.
6. `Customers[Country]` contains 46 raw spellings of 17 real countries. `data/Regions.csv` contains the canonical names.

## Preparation

- Confirm every learner has an updated Power BI Desktop installation on Windows.
- Confirm work or school Microsoft accounts, licences, and tenant access before the session.
- Create the cohort Power BI workspace. Give learners the minimum workspace role needed for the exercise; use Viewer accounts to validate RLS.
- Decide whether refresh will use an on-premises data gateway or SharePoint/OneDrive for work. Test credentials and refresh in advance.
- Ask learners to extract the kit to a short path and set import locale to English (United States).
- Keep `data/_later/Bookings_2026_H1.csv` outside `data/Bookings/` until the refresh exercise.
- If distributing a learner-specific archive, omit `answer_key.json` and this file. Do not refer to a data-generation script; none is included in this repository.
- Prepare catch-up `.pbix` files after data preparation, modelling, DAX, and report design.

## Dynamic RLS setup

The four `ManagerEmail` values in `data/Regions.csv` are synthetic and cannot sign in. Before a live dynamic-RLS demonstration, work on a separate teaching copy and replace them with volunteer learners' real work or school email addresses. Do not commit or redistribute that copy. Preserve the original repository data.

Test RLS with an account that has Viewer permission. Workspace Admins, Members, and Contributors have edit access and do not experience RLS like report viewers.

## Suggested timing

| Time (EAT) | Activity | Facilitation tip |
|---|---|---|
| 08:30–09:00 | Setup and scenario | Resolve Windows, account, locale, and file-path issues before teaching concepts |
| 09:00–09:40 | Stage 1: Get data | Pause after `DataFolder`; check that 2026 is not loaded |
| 09:40–10:40 | Stage 2: Clean | Give 15–20 minutes of unguided profiling before revealing solutions |
| 10:40–10:55 | Break | Save a clean-data catch-up file |
| 10:55–11:55 | Stage 3: Model | Ask learners to predict filter direction before creating each link |
| 11:55–13:00 | Stage 4: Core DAX | Validate after every two or three measures |
| 13:00–13:45 | Lunch | Save a model catch-up file |
| 13:45–14:30 | Stage 4: Remaining DAX | Demonstrate booking date versus travel date side by side |
| 14:30–15:45 | Stages 5–6: Report and interaction | Time-box formatting; prioritize accurate question-led visuals |
| 15:45–16:00 | Break | Pair learners for interaction testing |
| 16:00–16:45 | Stages 7–8: Security and Service | Keep a pre-published fallback if tenant or gateway setup fails |
| 16:45–17:30 | Stage 9: Insights | Enforce five minutes and require evidence, implication, action |

For four evening sessions, group Stages 1–3, Stage 4, Stages 5–6, and Stages 7–9. Start each evening from the prior catch-up file so slower learners can rejoin.

## Common student mistakes

| Mistake | Coaching response |
|---|---|
| Profiling only the first 1,000 rows | Point to the status-bar profiling option; ask the learner to compare distinct counts again |
| Loading `_later` during Stage 1 | Move it back and refresh; explain that it is the Stage 8 change event |
| Removing whole-row duplicates | Ask what the table grain and stable key are; deduplicate `BookingID` |
| Replacing empty strings but not nulls | Show the profile's Empty count and inspect the formula bar after replacement |
| Treating `DiscountPct` as 5 instead of 0.05 | Revisit locale and percentage formatting; validate Net Revenue |
| Connecting Customers directly to raw country spellings | Use an unmatched-country table and repair keys before modelling |
| Making every relationship bidirectional | Trace a filter from dimension to fact and discuss ambiguity |
| Activating both booking and travel date relationships | Keep BookingDate active and use `USERELATIONSHIP` for travel measures |
| Linking Reviews directly to Date | Trace the second path through Bookings; remove the direct relationship |
| Calculating tour cost with a plain `SUM` | Explain row iteration with `SUMX` and lookup with `RELATED` |
| Showing targets by day | Explain that targets exist only on each month's first day |
| Testing RLS as a workspace editor | Use View as in Desktop and a Viewer account in Service |
| Assuming region RLS filters targets | Ask learners to trace the Regions-to-Targets path; discuss regional targets or hiding the comparison |
| Scheduling “06:00” without checking time zone | Convert explicitly: 06:00 EAT is 03:00 UTC |
| Spending too long on colours | Require checkpoint accuracy first, then apply the supplied theme |

## Checkpoints and debrief

Use [`answer_key.json`](answer_key.json) for detailed verification. Reveal only the checkpoint appropriate to the current stage. Ask learners to explain the cause of a mismatch before giving them a completed query.

Useful critique prompts:

- What should the CEO understand from this page in five seconds?
- Which date is filtering this number?
- Which table owns this business definition?
- Can this pattern support a recommendation, or only a question for further investigation?
- What will a regional manager see, and what should they see?

If Service, gateway, map, or tenant policy blocks the live exercise, demonstrate the affected step with a prepared environment and let learners complete the local modelling evidence. Do not treat an infrastructure limitation as a modelling error.
