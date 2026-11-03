# tools/arca: offline helpers for a monotributista (Argentina)

Stdlib-only Python 3. Nothing here talks to the network or needs a fiscal key; inputs are files you export yourself. Not tax advice (see `docs/MONOTRIBUTO_SELF_AUDIT.md`).

| file | what it does |
|---|---|
| `category_calc.py` | sums the 12-month window of an issued-invoices CSV (credit notes subtract, foreign currency uses the rate column), says which category the income needs, and flags an exceeded current category. `--start` adds the annualised figures for an activity under 12 months old |
| `due_calendar.py` | writes an `.ics` with the monthly quota due date (shifted past weekends and holidays), a reminder for the monthly Convenio Multilateral return, and the January and July recategorisation reminders |
| `test_arca.py` | self-test on synthetic data: `python3 tools/arca/test_arca.py` |
| `data/monotributo_scales.json` | category caps and monthly totals, with `as_of` and source; refresh every semester |
| `data/holidays_*.json` | public holidays, from a community API; refresh each year |
| `VENDOR.md` | third-party ARCA tools considered, licence and static-audit notes (clones live in a git-ignored `vendor/`) |

## Examples

```
python3 tools/arca/category_calc.py invoices.csv --current A --as-of 2026-12-31
python3 tools/arca/category_calc.py invoices.csv --current A --as-of 2026-06-30 --start 2025-12-10   # activity under 12 months
python3 tools/arca/due_calendar.py --from 2026-11 --months 14 > monotributo.ics
```

CSV columns recognised (case and accents ignored): a date (`Fecha de Emision`), a document type (`Tipo Comprobante`), a total (`Imp. Total` or `Importe Total`), optionally a currency and an exchange rate. Delimiter `;`, `,` or tab. Amounts like `1.234,56` and `1,234.56` both parse.

## Limits

Only the income cap is checked (not rent, energy use, surface). The activity-age rule behind `--start` comes from press and is unverified. Keep real CSVs in `private/`, never in git.
